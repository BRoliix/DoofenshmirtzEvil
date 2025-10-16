#!/bin/bash

# 🚀 Streamlit Community Cloud CLI Deployment Script
# This script automates the deployment process for Streamlit Community Cloud

echo "🚀 Starting Streamlit Community Cloud deployment process..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}📋 Checking deployment requirements...${NC}"

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}❌ Error: Not in a git repository${NC}"
    exit 1
fi

# Check if we have uncommitted changes
if ! git diff --quiet || ! git diff --cached --quiet; then
    echo -e "${YELLOW}⚠️  Warning: You have uncommitted changes${NC}"
    echo "Do you want to commit them? (y/n)"
    read -r commit_choice
    if [ "$commit_choice" = "y" ] || [ "$commit_choice" = "Y" ]; then
        git add .
        echo "Enter commit message (or press enter for default):"
        read -r commit_msg
        if [ -z "$commit_msg" ]; then
            commit_msg="Deploy: Update app for Streamlit Community Cloud"
        fi
        git commit -m "$commit_msg"
    fi
fi

# Push to GitHub
echo -e "${BLUE}📤 Pushing to GitHub...${NC}"
git push origin main

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Successfully pushed to GitHub${NC}"
else
    echo -e "${RED}❌ Failed to push to GitHub${NC}"
    exit 1
fi

# Get repository info
REPO_URL=$(git remote get-url origin)
REPO_NAME=$(basename "$REPO_URL" .git)
REPO_OWNER=$(basename "$(dirname "$REPO_URL")" | sed 's/.*://')

echo -e "${GREEN}✅ Repository: $REPO_OWNER/$REPO_NAME${NC}"

# Check required files
echo -e "${BLUE}📋 Checking deployment files...${NC}"

required_files=("main.py" "requirements_streamlit.txt" ".streamlit/config.toml")
missing_files=()

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -ne 0 ]; then
    echo -e "${RED}❌ Missing required files:${NC}"
    printf '%s\n' "${missing_files[@]}"
    exit 1
fi

echo -e "${GREEN}✅ All required files present${NC}"

# Display deployment information
echo ""
echo -e "${GREEN}🎉 Ready for deployment!${NC}"
echo ""
echo -e "${BLUE}📋 Deployment Information:${NC}"
echo -e "Repository: ${YELLOW}$REPO_OWNER/$REPO_NAME${NC}"
echo -e "Branch: ${YELLOW}main${NC}"
echo -e "Main file: ${YELLOW}main.py${NC}"
echo -e "Requirements: ${YELLOW}requirements_streamlit.txt${NC}"
echo ""

# Option 1: Open Streamlit Share in browser
echo -e "${BLUE}🚀 Deployment Options:${NC}"
echo ""
echo -e "${GREEN}Option 1: Deploy via Web Interface (Recommended)${NC}"
echo "1. Open: https://share.streamlit.io/"
echo "2. Click 'New app'"
echo "3. Fill in the form:"
echo "   - Repository: $REPO_OWNER/$REPO_NAME"
echo "   - Branch: main"
echo "   - Main file path: main.py"
echo "4. Click 'Deploy!'"
echo ""

# Offer to open the browser
echo "Would you like to open Streamlit Share in your browser now? (y/n)"
read -r open_browser
if [ "$open_browser" = "y" ] || [ "$open_browser" = "Y" ]; then
    open "https://share.streamlit.io/"
fi

echo ""
echo -e "${GREEN}Option 2: Use Streamlit CLI (Local Testing)${NC}"
echo "Test your app locally before deployment:"
echo -e "${YELLOW}streamlit run main.py${NC}"

echo ""
echo -e "${BLUE}🔗 Your app will be available at:${NC}"
echo -e "${YELLOW}https://your-app-name.streamlit.app${NC}"
echo ""
echo -e "${GREEN}✨ Deployment process complete!${NC}"