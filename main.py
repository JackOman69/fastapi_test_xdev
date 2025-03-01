import asyncio
from app import app

async def main():
    from uvicorn import Config, Server

    config = Config(app, host="0.0.0.0", port=8010)
    server = Server(config)

    fastapi_task = asyncio.create_task(server.serve())

    await asyncio.gather(fastapi_task)
   
if __name__ == "__main__":
    asyncio.run(main())