#!/bin/bash

# Deployment Readiness Checker

echo "========================================"
echo "  Deployment Readiness Checker"
echo "========================================"
echo

# Check for required files
echo "📋 Checking required files..."
files=("Procfile" "runtime.txt" "requirements.txt" "app.py" "train_model.py" "models/house_price_model.pkl" "models/feature_names.pkl")

all_exist=true
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file"
    else
        echo "  ✗ $file (MISSING)"
        all_exist=false
    fi
done

echo

# Check for git
echo "📦 Checking Git setup..."
if command -v git &> /dev/null; then
    echo "  ✓ Git is installed"
    if [ -d ".git" ]; then
        echo "  ✓ Git repository initialized"
        remote=$(git config --get remote.origin.url)
        if [ -z "$remote" ]; then
            echo "  ⚠ No remote origin set (needed for deployment)"
        else
            echo "  ✓ Remote origin: $remote"
        fi
    else
        echo "  ✗ Git repository not initialized"
    fi
else
    echo "  ✗ Git is not installed"
fi

echo

# Check Python version
echo "🐍 Checking Python..."
if command -v python3 &> /dev/null; then
    py_version=$(python3 --version 2>&1 | awk '{print $2}')
    echo "  ✓ Python $py_version"
else
    echo "  ✗ Python 3 not found"
fi

echo

# Check dependencies
echo "📚 Checking dependencies..."
pip_packages=("flask" "scikit-learn" "numpy" "pandas" "gunicorn")
for package in "${pip_packages[@]}"; do
    if python3 -c "import ${package//'-'/'_'}" 2>/dev/null; then
        echo "  ✓ $package"
    else
        echo "  ⚠ $package (not installed locally, but will be installed on deployment)"
    fi
done

echo

# Summary
echo "========================================"
if [ "$all_exist" = true ]; then
    echo "✅ Ready for deployment!"
    echo
    echo "Next steps:"
    echo "1. Initialize Git: git init"
    echo "2. Push to GitHub"
    echo "3. Deploy to Render/Railway/Google Cloud"
    echo
    echo "See DEPLOY_QUICK.md for detailed instructions"
else
    echo "⚠ Some files are missing!"
    echo "Make sure you have trained the model: python train_model.py"
fi
echo "========================================"
