#!/usr/bin/env python3
"""
Usage Metrics Script for handson-ml2 Repository

This script fetches and displays usage metrics for the repository including:
- Repository statistics (stars, forks, watchers, open issues)
- Traffic data (views and clones) if available
- Repository size and last update information

Usage:
    python usage_metrics.py
    
Note: Traffic data requires repository owner/admin access via GitHub token.
Set GITHUB_TOKEN environment variable for full functionality.
"""

import requests
import os
from datetime import datetime, timezone
import sys


class UsageMetrics:
    def __init__(self, owner="ageron", repo="handson-ml2"):
        """
        Initialize the usage metrics fetcher.
        
        Args:
            owner: Repository owner (default: ageron)
            repo: Repository name (default: handson-ml2)
        """
        self.owner = owner
        self.repo = repo
        self.api_base = "https://api.github.com"
        self.token = os.environ.get("GITHUB_TOKEN")
        self.headers = {}
        
        if self.token:
            self.headers["Authorization"] = f"Bearer {self.token}"
    
    def get_repository_info(self):
        """Fetch basic repository information and statistics."""
        url = f"{self.api_base}/repos/{self.owner}/{self.repo}"
        
        try:
            response = requests.get(url, headers=self.headers)
            
            # Check rate limit
            if response.status_code == 403:
                if 'X-RateLimit-Remaining' in response.headers:
                    if response.headers['X-RateLimit-Remaining'] == '0':
                        reset_time = datetime.fromtimestamp(int(response.headers['X-RateLimit-Reset']), tz=timezone.utc)
                        print(f"⚠️  GitHub API rate limit exceeded. Resets at {reset_time.strftime('%Y-%m-%d %H:%M:%S')} UTC")
                        return None
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching repository info: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            return None
    
    def get_traffic_views(self):
        """Fetch repository traffic views (requires authentication and permissions)."""
        url = f"{self.api_base}/repos/{self.owner}/{self.repo}/traffic/views"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return None
    
    def get_traffic_clones(self):
        """Fetch repository traffic clones (requires authentication and permissions)."""
        url = f"{self.api_base}/repos/{self.owner}/{self.repo}/traffic/clones"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return None
    
    def get_popular_paths(self):
        """Fetch popular repository paths (requires authentication and permissions)."""
        url = f"{self.api_base}/repos/{self.owner}/{self.repo}/traffic/popular/paths"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return None
    
    def get_popular_referrers(self):
        """Fetch popular referrers (requires authentication and permissions)."""
        url = f"{self.api_base}/repos/{self.owner}/{self.repo}/traffic/popular/referrers"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return None
    
    def format_number(self, num):
        """Format large numbers with thousands separators."""
        return f"{num:,}"
    
    def display_metrics(self):
        """Display all available usage metrics."""
        print("=" * 70)
        print("REPOSITORY USAGE METRICS")
        print("=" * 70)
        print()
        
        # Get repository info
        repo_info = self.get_repository_info()
        
        if not repo_info:
            print("Failed to fetch repository information.")
            return
        
        # Display basic repository information
        print(f"Repository: {repo_info['full_name']}")
        print(f"Description: {repo_info.get('description', 'N/A')}")
        print()
        
        # Display repository statistics
        print("REPOSITORY STATISTICS")
        print("-" * 70)
        print(f"⭐ Stars:          {self.format_number(repo_info['stargazers_count'])}")
        print(f"🍴 Forks:          {self.format_number(repo_info['forks_count'])}")
        print(f"👁️  Watchers:       {self.format_number(repo_info['watchers_count'])}")
        print(f"📂 Size:           {self.format_number(repo_info['size'])} KB")
        print(f"❗ Open Issues:    {self.format_number(repo_info['open_issues_count'])}")
        print(f"🔀 Default Branch: {repo_info['default_branch']}")
        
        # Display last update
        updated_at = datetime.strptime(repo_info['updated_at'], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        print(f"🕒 Last Updated:   {updated_at.strftime('%Y-%m-%d %H:%M:%S')} UTC")
        
        # Display language
        if repo_info.get('language'):
            print(f"💻 Language:       {repo_info['language']}")
        
        # Display license
        if repo_info.get('license'):
            print(f"📜 License:        {repo_info['license']['name']}")
        
        print()
        
        # Try to get traffic data
        if self.token:
            print("TRAFFIC STATISTICS (Last 14 Days)")
            print("-" * 70)
            
            # Views
            views = self.get_traffic_views()
            if views:
                print(f"👀 Total Views:    {self.format_number(views.get('count', 0))}")
                print(f"👤 Unique Visitors: {self.format_number(views.get('uniques', 0))}")
            
            # Clones
            clones = self.get_traffic_clones()
            if clones:
                print(f"📥 Total Clones:   {self.format_number(clones.get('count', 0))}")
                print(f"👥 Unique Cloners: {self.format_number(clones.get('uniques', 0))}")
            
            if not views and not clones:
                print("⚠️  Traffic data not available (requires repository admin access)")
            
            print()
            
            # Popular paths
            popular_paths = self.get_popular_paths()
            if popular_paths and len(popular_paths) > 0:
                print("POPULAR FILES/PATHS")
                print("-" * 70)
                for i, path in enumerate(popular_paths[:10], 1):
                    print(f"{i}. {path['path']:<50} ({self.format_number(path['count'])} views)")
                print()
            
            # Popular referrers
            popular_referrers = self.get_popular_referrers()
            if popular_referrers and len(popular_referrers) > 0:
                print("TOP REFERRERS")
                print("-" * 70)
                for i, referrer in enumerate(popular_referrers[:10], 1):
                    print(f"{i}. {referrer['referrer']:<50} ({self.format_number(referrer['count'])} views)")
                print()
        else:
            print("TRAFFIC STATISTICS")
            print("-" * 70)
            print("⚠️  Set GITHUB_TOKEN environment variable to view traffic data")
            print("   (Traffic data requires repository owner/admin access)")
            print()
        
        print("=" * 70)
        print()
        print("📊 Metrics fetched successfully!")
        print()


def main():
    """Main function to run the usage metrics script."""
    # Parse command line arguments for custom owner/repo if needed
    owner = "ageron"
    repo = "handson-ml2"
    
    if len(sys.argv) > 1:
        owner = sys.argv[1]
    if len(sys.argv) > 2:
        repo = sys.argv[2]
    
    # Create metrics instance and display
    metrics = UsageMetrics(owner, repo)
    metrics.display_metrics()


if __name__ == "__main__":
    main()
