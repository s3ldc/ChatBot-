from aiohttp import web
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, MessageFactory
from botbuilder.schema import Activity


app_id = "5aa90243-c411-4c29-9aaf-d2ec8a149778"  
app_password = "72463fb3-0428-4645-bc25-4141e1c20f7b"  
adapter_settings = BotFrameworkAdapterSettings(app_id, app_password)
adapter = BotFrameworkAdapter(adapter_settings)


async def handle_message(context):
    if context.activity.type == "message":
        user_message = context.activity.text
        await context.send_activity(MessageFactory.text(f"You said: {user_message}"))
    else:
        await context.send_activity(MessageFactory.text(f"[{context.activity.type} event detected]"))


async def messages(request):
    body = await request.json()
    activity = Activity().deserialize(body)
    auth_header = request.headers.get("Authorization", "")
    response = await adapter.process_activity(activity, auth_header, handle_message)
    return web.Response(status=response.status)


app = web.Application()
app.router.add_post("/api/messages", messages)


if __name__ == "__main__":
    web.run_app(app, port=3978)
