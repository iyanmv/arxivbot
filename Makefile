all: LICENSE README.md arxivbot.py maubot.yaml
	zip -9r com.iyanmv.arxivbot-v$$(grep version maubot.yaml | cut -d " " -f 2).mbp LICENSE README.md arxivbot.py maubot.yaml
