# ⚙️ Setup Files

Get started with your **Python automation tools** to customize and launch your personal portfolio website effortlessly.

### 🐍 Install Python (If Not Already Installed)

Before running any Python scripts, ensure Python is installed on your system:

1. **Download Python** from the official site:
   👉 [https://www.python.org/downloads/](https://www.python.org/downloads/)

2. During installation, make sure to check ✅ **“Add Python to PATH”**.

3. Verify installation:

   ```bash
   python --version
   ```

   Or if you're on some Linux/Mac systems:

   ```bash
   python3 --version
   ```

### 🚀 Quick Start Guide

1. 📁 **Choose a Template:**
   Visit [`Templates.md`](../Templates.md) to explore available portfolio templates and themes. Pick the one that fits your style and purpose best.

2. 💾 **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. 🛠️ **Update JSON Data:**
   Run the following script to update necessary JSON configuration files:

   ```bash
   python JSON_Updation.py
   ```

   > If `python` doesn't work, try `python3` instead.

4. 🎨 **Select Your Template:**
   Execute:

   ```bash
   python Template_Selector.py
   ```

   > ⚠️ This will remove all other templates except the one you select.

5. 🧩 **Update Meta Tags:**
   Run:

   ```bash
   python Meta_Data_Updation.py
   ```

   Choose between:

   * ✅ JSON-driven automatic mode
   * ✍️ Manual entry mode

### 🌐 Test Locally Before Going Live

To preview your website locally, follow the guide:
📄 [`jekyll-localhost-setup.md`](../Localhost_Setup/jekyll-localhost-setup.md)

> A PDF version is also available.

### 🌍 Your Website Will Be Live At:

```
http://localhost:4000/Portfolio-Templates/
```

Or, based on the folder name you choose.

### ⚙️ Final Step – Update `_config.yml`

Make sure to update the `baseurl` field in `_config.yml` to match your selected folder name:

```yml
baseurl: "/Your-Folder-Name"
```