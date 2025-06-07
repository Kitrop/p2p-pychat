import asyncio
import json
import logging
from typing import Optional, Callable
from aiortc import RTCPeerConnection, RTCSessionDescription
from ..utils.config import STUN_SERVERS

logger = logging.getLogger(__name__)


class P2PConnection:
    def __init__(self, crypto_manager):
        self.pc: Optional[RTCPeerConnection] = None
        self.data_channel = None
        self.crypto = crypto_manager
        self._connected = False
        self.message_received = None
        self.connection_closed = None

    def set_callbacks(self, on_message, on_connection_closed):
        """Установка функций обратного вызова"""
        self.message_received = on_message
        self.connection_closed = on_connection_closed

    async def create_connection(self) -> None:
        """Создание нового P2P соединения"""
        self.pc = RTCPeerConnection({
            "iceServers": [{"urls": STUN_SERVERS}]
        })

        @self.pc.on("datachannel")
        def on_datachannel(channel):
            self.data_channel = channel
            self._connected = True

            @channel.on("message")
            def on_message(message):
                if isinstance(message, str) and self.message_received:
                    self.message_received(message)

        @self.pc.on("connectionstatechange")
        async def on_connectionstatechange():
            if self.pc.connectionState == "failed":
                await self.pc.close()
                self._connected = False
                if self.connection_closed:
                    self.connection_closed()

    async def create_offer(self) -> str:
        """Создание предложения для соединения"""
        if not self.pc:
            await self.create_connection()

        self.data_channel = self.pc.createDataChannel("chat")

        @self.data_channel.on("message")
        def on_message(message):
            if isinstance(message, str):
                self.message_received(message)

        offer = await self.pc.createOffer()
        await self.pc.setLocalDescription(offer)

        return json.dumps({
            "sdp": self.pc.localDescription.sdp,
            "type": self.pc.localDescription.type
        })

    async def handle_answer(self, answer: str) -> None:
        """Обработка ответа на предложение"""
        if not self.pc:
            raise RuntimeError("Соединение не создано")

        answer_dict = json.loads(answer)
        answer_desc = RTCSessionDescription(
            sdp=answer_dict["sdp"],
            type=answer_dict["type"]
        )
        await self.pc.setRemoteDescription(answer_desc)

    async def handle_offer(self, offer: str) -> str:
        """Обработка входящего предложения"""
        if not self.pc:
            await self.create_connection()

        offer_dict = json.loads(offer)
        offer_desc = RTCSessionDescription(
            sdp=offer_dict["sdp"],
            type=offer_dict["type"]
        )
        await self.pc.setRemoteDescription(offer_desc)

        answer = await self.pc.createAnswer()
        await self.pc.setLocalDescription(answer)

        return json.dumps({
            "sdp": self.pc.localDescription.sdp,
            "type": self.pc.localDescription.type
        })

    async def send_message(self, message: str) -> None:
        """Отправка сообщения через data channel"""
        if not self.data_channel or not self._connected:
            raise RuntimeError("Data channel не создан или не подключен")

        self.data_channel.send(message)

    async def close(self) -> None:
        """Закрытие соединения"""
        if self.pc:
            await self.pc.close()
            self._connected = False
            self.data_channel = None
            self.pc = None

    @property
    def is_connected(self) -> bool:
        """Проверка состояния соединения"""
        return self._connected and self.pc and self.pc.connectionState == "connected"
