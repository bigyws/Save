#!/bin/sh
# app.html(클로드 아티팩트용 본문)에 문서 머리말을 붙여 index.html(GitHub Pages용)을 만듭니다.
cd "$(dirname "$0")/.." || exit 1
{ printf '<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n<meta name="theme-color" content="#F7F4EE">\n</head>\n<body>\n'; cat app.html; printf '\n</body>\n</html>\n'; } > index.html
