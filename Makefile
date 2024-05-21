.PHONY: grpc clean
.DEFAULT_GOAL := help

ifndef ATUTILS_ROOT
$(error Please set up Python venv first using '`source bin/u-activate`')
endif

help:
	@echo "make deps	-- Install python dependencies and grpc definitions"
	@echo "make grpc	-- Download the protobuf/grpc definitions for anytype-heart and compile them into Python"
	@echo "make launch-app	-- Use Anytype's nativeMessaginHost program to launch Anytype (Mac only - patches accepted)"
	@echo "make get-ports	-- Use Anytype's nativeMessaginHost program to get Anytype ports (Mac only - patches accepted)"

grpc:
	bin/update-grpc

deps: grpc
	pip install -r requirements.txt

launch-app:
	@printf '\x15\0\0\0{"type": "launchApp"}' | '/Applications/Anytype.app/Contents/Resources/app.asar.unpacked/dist/nativeMessagingHost' | cut -c 5- | jq .

get-ports:
	@printf '\x14\0\0\0{"type": "getPorts"}' | '/Applications/Anytype.app/Contents/Resources/app.asar.unpacked/dist/nativeMessagingHost' | cut -c 5- | jq .
