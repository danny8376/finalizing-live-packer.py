#!/usr/bin/python3

#
# 3DS Guide Finalizing Setup packager
#
# SPDX-License-Identifier: 0BSD
#

import os
import shutil
from contextlib import asynccontextmanager

import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, RedirectResponse
from httpx import AsyncClient
from zipstream import AioZipStream

app = FastAPI()
client = AsyncClient(follow_redirects=True)

async def http_retrieve(url):
    async with client.stream('GET', url) as r:
        async for chunk in r.aiter_bytes(chunk_size=65536):
            yield chunk

async def pack_zip():
    files = [
        # {'stream': http_retrieve_gm9("https://github.com/d0k3/GodMode9/releases/download/v2.1.1/GodMode9-v2.1.1-20220322194259.zip"),
        #  'name': "luma/payloads/GodMode9.firm"},
        {'stream': http_retrieve("https://github.com/astronautlevel2/Anemone3DS/releases/latest/download/Anemone3DS.cia"),
         'name': "finalize/Anemone3DS.cia"},
        {'stream': http_retrieve("https://github.com/astronautlevel2/Anemone3DS/releases/latest/download/Anemone3DS.cia"),
         'name': "finalize/Anemone3DS.cia"},
        {'stream': http_retrieve("https://github.com/BernardoGiordano/Checkpoint/releases/download/v3.7.4/Checkpoint.cia"),
         'name': "finalize/Checkpoint.cia"},
        {'stream': http_retrieve("https://github.com/PabloMK7/homebrew_launcher_dummy/releases/latest/download/Homebrew_Launcher.cia"),
         'name': "finalize/Homebrew_Launcher.cia"},
        {'stream': http_retrieve("https://github.com/Steveice10/FBI/releases/latest/download/FBI.cia"),
         'name': "finalize/FBI.cia"},
        {'stream': http_retrieve("https://github.com/mtheall/ftpd/releases/latest/download/ftpd.cia"),
         'name': "finalize/ftpd.cia"},
        {'stream': http_retrieve("https://github.com/Universal-Team/Universal-Updater/releases/latest/download/Universal-Updater.cia"),
         'name': "finalize/Universal-Updater.cia"},
        # {'stream': http_retrieve(""),
        #  'name': ""},
    ]
    aiozip = AioZipStream(files, chunksize=32768)
    async for chunk in aiozip.stream():
        yield chunk

@app.get("/finalize")
async def finalize():
    return StreamingResponse(pack_zip())


@app.get("/", include_in_schema=False)
async def webpage():
    return RedirectResponse("https://3ds.hacks.guide")
