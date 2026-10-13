.PHONY: help serve dev build deploy status

HUGO_DIR = receps_blog
PUBLIC_DIR = ../../erolrecep.github.io

help:
	@echo "📚 Personal Blog (Source) - Command Center"
	@echo "------------------------------------------"
	@echo "  make serve   - Run Hugo development server with drafts (http://localhost:1313)"
	@echo "  make build   - Build production site directly into erolrecep.github.io"
	@echo "  make deploy  - Build and push updates to GitHub Pages (erolrecep.github.io)"
	@echo "  make status  - Check git status across source and public repos"

serve: dev

dev:
	@echo "🚀 Starting Hugo local development server..."
	cd $(HUGO_DIR) && hugo server -D --bind 127.0.0.1 -p 1313

build:
	@echo "🔨 Building production site into erolrecep.github.io..."
	cd $(HUGO_DIR) && hugo --destination $(PUBLIC_DIR) --cleanDestinationDir
	@echo "✅ Build completed successfully into erolrecep.github.io!"

status:
	@echo "📌 Source Repo (blog):"
	@git status -s
	@echo ""
	@echo "🌐 Public Pages Repo (erolrecep.github.io):"
	@cd ../erolrecep.github.io && git status -s

deploy: build
	@echo "🚀 Staging and committing in erolrecep.github.io..."
	@cd ../erolrecep.github.io && git add -A && git commit -m "Update blog content" || echo "No changes to commit"
	@echo "📤 Pushing to GitHub Pages (main)..."
	@cd ../erolrecep.github.io && git push origin main
	@echo "🎉 Deployed live to https://erolrecep.github.io!"
