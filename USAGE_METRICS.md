# Usage Metrics

This directory contains scripts to view usage metrics for the handson-ml2 repository.

## Available Scripts

### 1. Local Usage Metrics (`local_usage_metrics.py`)

Analyzes the local git repository and provides comprehensive metrics including:
- Repository information (path, branch, remote URL)
- Commit statistics (total commits, contributors)
- Recent commit history
- File statistics (file count, total size)
- Jupyter notebook analysis (count, sizes, largest notebooks)
- File type distribution

**Usage:**
```bash
python local_usage_metrics.py
```

**Example Output:**
```
======================================================================
LOCAL REPOSITORY USAGE METRICS
======================================================================

REPOSITORY INFORMATION
----------------------------------------------------------------------
📁 Path:           /path/to/handson-ml2
🌿 Current Branch: master
🔗 Remote URL:     https://github.com/ageron/handson-ml2

COMMIT STATISTICS
----------------------------------------------------------------------
📝 Total Commits:  500+

TOP CONTRIBUTORS
----------------------------------------------------------------------
1. Contributor Name                         (300 commits)
...

JUPYTER NOTEBOOKS
----------------------------------------------------------------------
📓 Total Notebooks: 27
💾 Total Size:      31.97 MB

Largest Notebooks:
1. 17_autoencoders_and_gans.ipynb           6.27 MB
...
```

**Features:**
- ✅ Works offline (no internet connection required)
- ✅ No authentication needed
- ✅ Fast analysis of local repository
- ✅ Detailed notebook statistics

### 2. GitHub API Usage Metrics (`usage_metrics.py`)

Fetches usage metrics from GitHub API including:
- Repository statistics (stars, forks, watchers, issues)
- Repository size and last update
- Traffic data (views and clones) - requires authentication
- Popular files/paths - requires authentication
- Top referrers - requires authentication

**Usage:**
```bash
# Default: ageron/handson-ml2
python usage_metrics.py

# Custom repository
python usage_metrics.py <owner> <repo>

# With GitHub token for traffic data
GITHUB_TOKEN=your_token_here python usage_metrics.py
```

**Example Output:**

*Note: The numbers shown below are example values for illustration purposes.*

```
======================================================================
REPOSITORY USAGE METRICS
======================================================================

Repository: ageron/handson-ml2
Description: Hands-on Machine Learning with Scikit-Learn, Keras and TensorFlow

REPOSITORY STATISTICS
----------------------------------------------------------------------
⭐ Stars:          45,000
🍴 Forks:          20,000
👁️  Watchers:       2,500
📂 Size:           36,000 KB
❗ Open Issues:    50
...
```

**Features:**
- 📊 Public repository statistics (no auth required)
- 🔐 Traffic data with GitHub token
- 📈 Popular paths and referrers with admin access
- 🌐 Works with any GitHub repository

## Requirements

Both scripts require **Python 3.7+** (for f-strings and other modern features).

The `local_usage_metrics.py` script uses only Python standard library modules (no additional dependencies required).

The `usage_metrics.py` script requires the `requests` library.

Install the requests library:
```bash
pip install requests
```

Or if using conda:
```bash
conda install requests
```

Note: The `requests` library is already included in the `requirements.txt` file for this repository.

## GitHub Token Setup

To access traffic data and other authenticated endpoints, you need a GitHub personal access token:

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate a new token with `repo` scope
3. Set the token as an environment variable:
   ```bash
   export GITHUB_TOKEN=your_token_here
   ```

## Which Script to Use?

- **Use `local_usage_metrics.py`** when:
  - You want to analyze your local repository
  - You don't need GitHub-specific metrics (stars, forks)
  - You want to work offline
  - You want notebook-specific analysis

- **Use `usage_metrics.py`** when:
  - You want to see GitHub engagement metrics (stars, forks, watchers)
  - You want to see traffic data (with authentication)
  - You want to analyze any GitHub repository (not just local)

## Examples

### View local repository metrics
```bash
cd /path/to/handson-ml2
python local_usage_metrics.py
```

### View GitHub repository metrics
```bash
# Current repository
python usage_metrics.py ageron handson-ml2

# Another repository
python usage_metrics.py tensorflow tensorflow
```

### View traffic data (requires token)
```bash
export GITHUB_TOKEN=your_token_here
python usage_metrics.py ageron handson-ml2
```

## Troubleshooting

### "Error fetching repository info: 403"
- This usually means you've hit the GitHub API rate limit
- Wait an hour or authenticate with a GitHub token
- Unauthenticated requests are limited to 60/hour

### "Traffic data not available"
- Traffic data requires repository owner/admin access
- Make sure you have a valid `GITHUB_TOKEN` set
- Make sure your token has the `repo` scope

### "Failed to fetch repository information"
- Check your internet connection (for `usage_metrics.py`)
- Verify the repository owner and name are correct
- Check if the repository is public and accessible

## License

These scripts are provided as part of the handson-ml2 repository and follow the same license.
