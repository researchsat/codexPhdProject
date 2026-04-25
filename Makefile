.PHONY: install run process-pdfs qa clean

install:
	python3 -m pip install -e .

run:
	ilm-wiki run --pdf-dir data/pdfs --manual-dir data/manual_records --output-dir output

process-pdfs:
	ilm-wiki process-pdfs --pdf-dir data/pdfs --output output/pdf_extractions.json

qa:
	ilm-wiki qa --output-dir output

clean:
	rm -rf output/*

