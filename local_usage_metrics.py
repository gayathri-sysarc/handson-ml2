#!/usr/bin/env python3
"""
Local Usage Metrics Script for handson-ml2 Repository

This script analyzes the local git repository and provides metrics including:
- Repository statistics (commits, contributors, files)
- File type distribution
- Notebook count and sizes
- Recent activity

Usage:
    python local_usage_metrics.py
"""

import os
import subprocess
import json
from datetime import datetime
from pathlib import Path
from collections import Counter, defaultdict


class LocalUsageMetrics:
    def __init__(self, repo_path=None):
        """
        Initialize the local usage metrics analyzer.
        
        Args:
            repo_path: Path to the git repository (default: current directory)
        """
        self.repo_path = repo_path or os.getcwd()
        
    def run_git_command(self, cmd):
        """Run a git command and return the output."""
        try:
            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return None
    
    def get_commit_count(self):
        """Get total number of commits."""
        output = self.run_git_command(['git', 'rev-list', '--all', '--count'])
        return int(output) if output else 0
    
    def get_contributors(self):
        """Get list of contributors and their commit counts."""
        output = self.run_git_command(['git', 'shortlog', '-sn', '--all'])
        if not output:
            return []
        
        contributors = []
        for line in output.split('\n'):
            if line.strip():
                parts = line.strip().split('\t', 1)
                if len(parts) == 2:
                    count = int(parts[0].strip())
                    name = parts[1].strip()
                    contributors.append({'name': name, 'commits': count})
        
        return contributors
    
    def get_recent_commits(self, count=10):
        """Get recent commits."""
        output = self.run_git_command([
            'git', 'log', 
            f'-{count}',
            '--pretty=format:%h|%an|%ar|%s'
        ])
        
        if not output:
            return []
        
        commits = []
        for line in output.split('\n'):
            if '|' in line:
                parts = line.split('|', 3)
                if len(parts) == 4:
                    commits.append({
                        'hash': parts[0],
                        'author': parts[1],
                        'date': parts[2],
                        'message': parts[3]
                    })
        
        return commits
    
    def get_file_statistics(self):
        """Analyze file types and sizes in the repository."""
        stats = {
            'total_files': 0,
            'by_extension': Counter(),
            'by_type': defaultdict(lambda: {'count': 0, 'size': 0}),
            'notebooks': [],
            'total_size': 0
        }
        
        # Walk through repository
        for root, dirs, files in os.walk(self.repo_path):
            # Skip .git directory
            if '.git' in root:
                continue
            
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, self.repo_path)
                
                try:
                    size = os.path.getsize(file_path)
                    stats['total_files'] += 1
                    stats['total_size'] += size
                    
                    # Get extension
                    ext = os.path.splitext(file)[1].lower()
                    if ext:
                        stats['by_extension'][ext] += 1
                        stats['by_type'][ext]['count'] += 1
                        stats['by_type'][ext]['size'] += size
                    
                    # Track notebooks separately
                    if ext == '.ipynb':
                        stats['notebooks'].append({
                            'path': rel_path,
                            'size': size,
                            'name': file
                        })
                
                except OSError:
                    continue
        
        return stats
    
    def get_repository_info(self):
        """Get basic repository information."""
        remote_url = self.run_git_command(['git', 'config', '--get', 'remote.origin.url'])
        current_branch = self.run_git_command(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
        
        return {
            'remote_url': remote_url,
            'current_branch': current_branch,
            'path': self.repo_path
        }
    
    def format_size(self, size_bytes):
        """Format bytes to human-readable size."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"
    
    def format_number(self, num):
        """Format large numbers with thousands separators."""
        return f"{num:,}"
    
    def display_metrics(self):
        """Display all available usage metrics."""
        print("=" * 70)
        print("LOCAL REPOSITORY USAGE METRICS")
        print("=" * 70)
        print()
        
        # Repository info
        repo_info = self.get_repository_info()
        print("REPOSITORY INFORMATION")
        print("-" * 70)
        print(f"📁 Path:           {repo_info['path']}")
        print(f"🌿 Current Branch: {repo_info['current_branch']}")
        if repo_info['remote_url']:
            print(f"🔗 Remote URL:     {repo_info['remote_url']}")
        print()
        
        # Commit statistics
        print("COMMIT STATISTICS")
        print("-" * 70)
        commit_count = self.get_commit_count()
        print(f"📝 Total Commits:  {self.format_number(commit_count)}")
        print()
        
        # Contributors
        contributors = self.get_contributors()
        if contributors:
            print("TOP CONTRIBUTORS")
            print("-" * 70)
            for i, contributor in enumerate(contributors[:10], 1):
                print(f"{i}. {contributor['name']:<40} ({self.format_number(contributor['commits'])} commits)")
            print()
        
        # Recent commits
        recent_commits = self.get_recent_commits(5)
        if recent_commits:
            print("RECENT COMMITS")
            print("-" * 70)
            for commit in recent_commits:
                print(f"• {commit['hash']} - {commit['date']}")
                print(f"  {commit['author']}: {commit['message'][:60]}")
            print()
        
        # File statistics
        file_stats = self.get_file_statistics()
        print("FILE STATISTICS")
        print("-" * 70)
        print(f"📄 Total Files:    {self.format_number(file_stats['total_files'])}")
        print(f"💾 Total Size:     {self.format_size(file_stats['total_size'])}")
        print()
        
        # Notebook statistics
        notebooks = file_stats['notebooks']
        if notebooks:
            print("JUPYTER NOTEBOOKS")
            print("-" * 70)
            print(f"📓 Total Notebooks: {len(notebooks)}")
            total_notebook_size = sum(nb['size'] for nb in notebooks)
            print(f"💾 Total Size:      {self.format_size(total_notebook_size)}")
            print()
            
            # Largest notebooks
            largest_notebooks = sorted(notebooks, key=lambda x: x['size'], reverse=True)[:10]
            print("Largest Notebooks:")
            for i, nb in enumerate(largest_notebooks, 1):
                print(f"{i}. {nb['name']:<50} {self.format_size(nb['size']):>12}")
            print()
        
        # File type distribution
        print("FILE TYPE DISTRIBUTION")
        print("-" * 70)
        sorted_extensions = sorted(
            file_stats['by_type'].items(),
            key=lambda x: x[1]['count'],
            reverse=True
        )[:15]
        
        for ext, data in sorted_extensions:
            ext_display = ext if ext else '(no extension)'
            print(f"{ext_display:<15} {self.format_number(data['count']):>6} files   {self.format_size(data['size']):>12}")
        
        print()
        print("=" * 70)
        print()
        print("📊 Metrics analyzed successfully!")
        print()


def main():
    """Main function to run the local usage metrics script."""
    import sys
    
    repo_path = sys.argv[1] if len(sys.argv) > 1 else None
    
    metrics = LocalUsageMetrics(repo_path)
    metrics.display_metrics()


if __name__ == "__main__":
    main()
