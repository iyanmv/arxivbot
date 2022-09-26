import aiohttp
import datetime
from bs4 import BeautifulSoup
from maubot import Plugin
from maubot.handlers import command


class ArXivBot(Plugin):

    @staticmethod
    async def _request(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                html = await response.text()
                return html

    @staticmethod
    def _output_text(d):
        msg = (
            f'**Date**: {d["date"]}\n\n'
            f'**Title**: {d["title"]}\n\n'
            f'**Authors**: {d["authors"]}\n\n'
            f'**Abstract**: {d["abstract"]}\n\n'
            f'**PDF**: {d["pdf"]}'
        )
        return msg

    async def _parse_arxiv(self, url):
        xml = await self._request(url)
        soup = BeautifulSoup(xml, features="xml")
        authors = []
        for elem in soup.head.find_all("meta"):
            try:
                name = elem["name"]
            except KeyError:
                pass
            if name == "citation_title":
                title = elem["content"]
            elif name == "citation_author":
                author = elem["content"].split(", ")
                authors.append(" ".join([author[-1], author[0]]))
            elif name == "citation_date":
                date = datetime.datetime.strptime(elem["content"], "%Y/%m/%d")
                date = date.strftime("%d.%m.%Y")
            elif name == "citation_pdf_url":
                pdf = elem["content"]
            elif name == "citation_abstract":
                abstract = elem["content"].strip()
        authors = ", ".join(authors)
        return {"title": title, "authors": authors, "date": date, "abstract": abstract, "pdf": pdf}

    @command.passive(r'(https?://arxiv\.org/abs/(?:quant-ph/)?[0-9\.]+)', multiple=True, multiline=True)
    async def arxiv(self, evt, matches):
        for _, match in matches:
            d = await self._parse_arxiv(match)
            out = self._output_text(d)
            await evt.reply(out, markdown=True)
