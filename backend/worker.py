import asyncio
import mimetypes
from EdgeGPT import Chatbot, ConversationStyle

import database
from utils import *

new_template = '''
Give Me {mime} Code for a website at /{slug} that does {description}.
Wrap the output in DELIMITER.
Do not return anything other than the code.
When generating javascript, keep variable names small and remove comments and extra newlines.
'''

revise_template = '''
Revise This {mime} Code at /{slug}
```
{code}
```
as such: {revision}.
Wrap the output in DELIMITER.
Do not return anything other than the code.
When generating javascript, keep variable names small and remove comments and extra newlines.
'''

async def new_page(slug, description):
    bot = Chatbot(cookiePath=cookies())
    mime, _ = mimetypes.guess_type(slug)
    mime = mime or 'text/html'
    old_doc = database.get_database()['pages'].find_one({'slug': slug})
    if old_doc is None:
        bot.close()
        return
    print(slug)
    response = await bot.ask(prompt=new_template.format(
        mime = mime,
        slug = slug,
        description = description
    ), conversation_style=ConversationStyle.creative)
    try:
        content = response['item']['messages'][1]['text']
        print(repr(content))
        content = content[:content.rindex('DELIMITER')]
        content = content[content.rindex('DELIMITER') + len('DELIMITER'):]
        content = content.strip()
        content = content.strip('```')
        print(repr(content))
    except:
        content = '<h1>AI Failed, please revise</h1><p>' + description + '</p>'
    database.get_database()['pages'].update_one({
        '_id': old_doc['_id']
    }, {
        '$set': {
            'content': content,
            'pending': False
        }
    })
    await bot.close()

async def revise_page(slug, revision):
    bot = Chatbot(cookiePath=cookies())
    mime, _ = mimetypes.guess_type(slug)
    mime = mime or 'text/html'
    old_doc = database.get_database()['pages'].find_one({'slug': slug})
    if old_doc is None:
        bot.close()
        return
    print(slug)
    response = await bot.ask(prompt=revise_template.format(
        mime = mime,
        slug = slug,
        code = old_doc['content'],
        revision = revision
    ), conversation_style=ConversationStyle.creative)
    try:
        content = response['item']['messages'][1]['text']
        print(repr(content))
        content = content[:content.rindex('DELIMITER')]
        content = content[content.rindex('DELIMITER') + len('DELIMITER'):]
        content = content.strip()
        content = content.strip('```')
        print(repr(content))
    except:
        content = old_doc['content']
    database.get_database()['pages'].update_one({
        '_id': old_doc['_id']
    }, {
        '$set': {
            'content': content,
            'pending': False
        }
    })
    await bot.close()

def run_worker(slug, description=None, revision=None):
    if description:
        @schedule(once=True)
        def worker():
            asyncio.run(new_page(slug, description))
    elif revision:
        @schedule(once=True)
        def worker():
            asyncio.run(revise_page(slug, revision))
