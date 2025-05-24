# GitHub Deployment Instructions

## Option 1: Using GitHub Web Interface (Recommended since Git is not installed locally)

### Step 1: Create a New Repository on GitHub
1. Go to [GitHub.com](https://github.com) and sign in
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Repository settings:
   - **Repository name**: `azure-diagram-mcp-server` or `genaidiagramsasmcp`
   - **Description**: "MCP server that generates Azure architecture diagrams from natural language descriptions"
   - **Visibility**: Public (recommended) or Private
   - **Initialize**: Do NOT check "Add a README file" (we already have one)
   - **Add .gitignore**: None (we already have one)
   - **Choose a license**: None (we already have one)
5. Click "Create repository"

### Step 2: Upload Files via GitHub Web Interface
1. On your new repository page, click "uploading an existing file"
2. Drag and drop ALL files from your `C:\learn\genaidiagramsasmcp\` folder:
   - `azure_diagram_server.py`
   - `requirements.txt`
   - `Dockerfile`
   - `README.md`
   - `.gitignore`
   - `.env.example`
   - `LICENSE`
   - `DEPLOYMENT_SUMMARY.md`
   - `tests/` folder (upload the entire folder)
3. Add a commit message: "Initial commit: Azure diagram MCP server with Docker support"
4. Click "Commit changes"

### Step 3: Update Repository Settings (Optional)
1. Go to Settings > General
2. Add topics/tags: `mcp`, `azure`, `diagrams`, `python`, `docker`, `architecture`
3. Add a website URL if you plan to deploy this
4. Enable Issues and Projects if you want community contributions

## Option 2: Install Git and Use Command Line

### Step 1: Install Git
Download and install Git from: https://git-scm.com/download/win

### Step 2: Initialize Repository and Push
```bash
cd C:\learn\genaidiagramsasmcp

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Azure diagram MCP server with Docker support"

# Add remote origin (replace with your actual repository URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Option 3: Using GitHub Desktop (User-Friendly GUI)

### Step 1: Install GitHub Desktop
Download from: https://desktop.github.com/

### Step 2: Add Repository
1. Open GitHub Desktop
2. File > Add Local Repository
3. Choose the `C:\learn\genaidiagramsasmcp` folder
4. Click "create a repository" if prompted
5. Add all files to the commit
6. Add commit message: "Initial commit: Azure diagram MCP server with Docker support"
7. Click "Publish repository" and choose public/private

## Next Steps After Upload

### 1. Update README with Correct Repository URL
Edit the README.md file and replace `<your-repo-url>` with your actual repository URL.

### 2. Create GitHub Actions for CI/CD (Optional)
Consider adding automated testing and Docker image building.

### 3. Add GitHub Pages Documentation (Optional)
You can enable GitHub Pages to host documentation.

### 4. Set Up Docker Hub Integration (Optional)
Configure automatic Docker image builds on Docker Hub.

## Repository Structure After Upload
```
your-repo/
├── azure_diagram_server.py     # Main MCP server
├── requirements.txt            # Dependencies
├── Dockerfile                  # Container config
├── README.md                   # Documentation
├── .gitignore                  # Git ignore rules
├── .env.example                # Environment template
├── LICENSE                     # MIT license
├── DEPLOYMENT_SUMMARY.md       # Deployment docs
└── tests/                      # Test files
    ├── __init__.py
    ├── test_server_fixed.py
    ├── validate_mcp.py
    └── test_mcp_simple.py
```

## Additional Recommendations

### 1. Add GitHub Repository Topics
Add these topics to help others discover your repository:
- `mcp-server`
- `azure`
- `architecture-diagrams`
- `python`
- `docker`
- `model-context-protocol`
- `azure-diagrams`
- `nlp`
- `graphviz`

### 2. Create GitHub Issues Templates (Optional)
Add issue templates for bug reports and feature requests.

### 3. Add Contributing Guidelines (Optional)
Create a `CONTRIBUTING.md` file with contribution guidelines.

### 4. Set Up Branch Protection Rules (Optional)
Protect the main branch to require pull request reviews.
