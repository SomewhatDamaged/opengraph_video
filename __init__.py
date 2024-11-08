from aiohttp import web

PORT = 8020

PATREON_DETAILS = {
    "name": "SourceBot",
    "url": "https://www.patreon.com/SourceBot"
}

DOMAIN = "http://excessive.space"

PATH = "/video"

OPENGRAPH = """<!DOCTYPE html>
<html>
<head>
<meta charset=\"utf-8\">
<meta property=\"og:type\" content=\"video.other\">
<title></title>
<meta property="og:url" content="{url}">
<meta property="og:title" content=" ">
<meta property="og:site_name" content=" ">
<meta property="og:image" content="">
<meta property="og:video" content="{url}">
<meta property="og:description" content=" ">
<link rel="alternate" type="application/json+oembed" href="{domain}{path}/oembed.json?url={url}" title="Damaged">
</head>
<body>
</body>
</html>
"""

def add_content_type(input: str, content_type: str) -> str:
    return input.replace("</head>", f"<meta property=\"og:video:type\" content=\"video/{content_type}\">\n</head>", 1)

def format_HTML(input: str, url: str) -> str:
    return input.format(url=url, domain=DOMAIN, path=PATH)

async def do_video(request: web.Request):
    url = request.query_string[4:].replace("\"", "&quot;")
    return web.Response(content_type="text/html", body=format_HTML(OPENGRAPH, url))

async def do_oembed(request: web.Request):
    url = request.query_string[4:].replace("\"", "&quot;")
    return web.json_response({
        "version": "1.0",
        "type": "rich",
        "title": " ",
        "author_name": "Video Link",
        "author_url": url,
        "provider_name": PATREON_DETAILS["name"],
        "provider_url": PATREON_DETAILS["url"],
        "url": url
        }
    )

async def do_video_forceformat(request: web.Request):
    url = request.query_string[4:].replace("\"", "&quot;")
    format = request.match_info['format'].replace("\"", "&quot;")
    html = add_content_type(OPENGRAPH, format)
    return web.Response(content_type="text/html", body=format_HTML(html, url))

def main():
    try:
        app = web.Application()
        app.add_routes([web.get(f'{PATH}/{{format}}',do_video_forceformat)])
        app.add_routes([web.get(f'{PATH}/oembed.json',do_oembed)])
        app.add_routes([web.get(f'{PATH}',do_video)])
        web.run_app(app, host="127.0.0.1", port=PORT)
    except Exception as e:
        print(e)
    
if __name__ == '__main__':
    main()
