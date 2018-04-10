from app.async_consumers import parser
import uuid
import asyncio


if __name__ == "__main__":
	uid = uuid.uuid4()
	
	loop = asyncio.get_event_loop()
	loop.run_until_complete(
		parser(username="vkozulya")
		)