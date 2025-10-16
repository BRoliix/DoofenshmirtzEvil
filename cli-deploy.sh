#!/bin/bash

# 🚀 Direct CLI Deployment to Streamlit Community Cloud
# This script uses direct API calls to deploy your app

echo "🚀 Direct CLI Deployment to Streamlit Community Cloud"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Repository info
REPO_OWNER="BRoliix"
REPO_NAME="DoofenshmirtzEvil"
BRANCH="main"
MAIN_FILE="main.py"

echo -e "${BLUE}📋 Deployment Configuration:${NC}"
echo -e "Repository: ${YELLOW}$REPO_OWNER/$REPO_NAME${NC}"
echo -e "Branch: ${YELLOW}$BRANCH${NC}"
echo -e "Main file: ${YELLOW}$MAIN_FILE${NC}"
echo ""

# Method 1: Direct URL approach
echo -e "${GREEN}🚀 Method 1: Direct URL Deployment${NC}"
echo ""
echo "You can deploy directly using this URL:"
DEPLOY_URL="https://share.streamlit.io/deploy?repository=$REPO_OWNER/$REPO_NAME&branch=$BRANCH&mainModule=$MAIN_FILE"
echo -e "${YELLOW}$DEPLOY_URL${NC}"
echo ""

# Method 2: cURL API approach
echo -e "${GREEN}🚀 Method 2: API Deployment (Advanced)${NC}"
echo ""

# Check if user wants to try API deployment
echo "Would you like to try automated API deployment? (y/n)"
read -r api_choice

if [ "$api_choice" = "y" ] || [ "$api_choice" = "Y" ]; then
    echo -e "${BLUE}🔐 Note: This requires Streamlit authentication${NC}"
    echo "You'll need to:"
    echo "1. Get your Streamlit API token from: https://share.streamlit.io/settings"
    echo "2. Enter it when prompted"
    echo ""
    
    echo "Enter your Streamlit API token (or press enter to skip):"
    read -r -s API_TOKEN
    
    if [ -n "$API_TOKEN" ]; then
        echo -e "${BLUE}📤 Deploying via API...${NC}"
        
        # Create deployment payload
        PAYLOAD=$(cat <<EOF
{
    "repository": "$REPO_OWNER/$REPO_NAME",
    "branch": "$BRANCH", 
    "mainModule": "$MAIN_FILE"
}
EOF
)

        # Make API call (Note: This is a simplified example, actual Streamlit API may differ)
        RESPONSE=$(curl -s -X POST \
            -H "Authorization: Bearer $API_TOKEN" \
            -H "Content-Type: application/json" \
            -d "$PAYLOAD" \
            "https://api.streamlit.io/v1/apps" 2>/dev/null)
            
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ API call successful${NC}"
            echo "Response: $RESPONSE"
        else
            echo -e "${YELLOW}⚠️  API deployment not available, using direct URL method${NC}"
        fi
    fi
fi

# Method 3: Open direct deployment URL
echo ""
echo -e "${GREEN}🚀 Method 3: Open Deployment URL${NC}"
echo "Would you like to open the deployment URL in your browser? (y/n)"
read -r open_choice

if [ "$open_choice" = "y" ] || [ "$open_choice" = "Y" ]; then
    echo -e "${BLUE}🌐 Opening deployment URL...${NC}"
    open "$DEPLOY_URL" 2>/dev/null || echo "Please manually open: $DEPLOY_URL"
fi

echo ""
echo -e "${GREEN}🎯 Manual Deployment Steps:${NC}"
echo "If the automated methods don't work, follow these steps:"
echo ""
echo "1. Go to: https://share.streamlit.io/"
echo "2. Sign in with GitHub"
echo "3. Click 'New app'"
echo "4. Fill in:"
echo "   - Repository: $REPO_OWNER/$REPO_NAME"
echo "   - Branch: $BRANCH"
echo "   - Main file path: $MAIN_FILE"
echo "5. Click 'Deploy!'"
echo ""

echo -e "${BLUE}📱 Your app will be available at:${NC}"
APP_URL=$(echo "$REPO_NAME" | tr '[:upper:]' '[:lower:]')
echo -e "${YELLOW}https://$APP_URL.streamlit.app${NC}"
echo ""

echo -e "${GREEN}✨ CLI deployment process complete!${NC}"
echo -e "${BLUE}💡 Tip: Bookmark your app URL for easy access${NC}"