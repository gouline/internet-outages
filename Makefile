SHELL := /bin/bash
ACTIVATE_VENV := true

-include .credentials.env
export

.PHONY: default
default: venv requirements run

venv:
	$(eval ACTIVATE_VENV := . .venv/bin/activate)
	[ -d .venv ] || ( python3 -m venv .venv \
		&& $(ACTIVATE_VENV) && pip3 install pip==21.1.2  )

.PHONY: requirements
requirements:
	( $(ACTIVATE_VENV) && pip3 install -r requirements.txt )

.PHONY: run
run:
	( $(ACTIVATE_VENV) && python3 -m outages )

.PHONY: test
test:
	( $(ACTIVATE_VENV) && python3 -m unittest tests )

clean:
	-rm -rf .venv build dist
