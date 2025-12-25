"""
GitHub API 客户端（异步版本）
提供 GitHub API 请求功能
使用 aiohttp 进行异步 HTTP 请求
"""
import os
from typing import Dict, Optional
from dotenv import load_dotenv
import aiohttp

# 加载环境变量
load_dotenv()

# GitHub API 基础 URL
GITHUB_API_BASE = "https://api.github.com"

# 从环境变量获取 GitHub Token（可选，但可以提高 API 限制）
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# 从环境变量获取 GitHub Username（可选，会添加到请求头中）
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")


def get_headers(username: Optional[str] = None) -> Dict[str, str]:
    """
    获取请求头，包含认证信息和用户名
    
    Args:
        username: 可选的 GitHub 用户名，如果不提供则从环境变量 GITHUB_USERNAME 读取
    
    Returns:
        包含请求头的字典
    """
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "GitHub-API-Client"
    }
    
    # 添加认证 Token
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    
    # 添加用户名到请求头（优先使用传入的 username，其次使用环境变量）
    final_username = username or GITHUB_USERNAME
    if final_username:
        headers["X-GitHub-Username"] = final_username
    
    return headers


async def github_api_request(url: str, params: Optional[Dict] = None, method: str = "GET", username: Optional[str] = None) -> Dict:
    """
    通用的 GitHub API 异步请求函数（使用 aiohttp）
    
    Args:
        url: 请求的 URL（可以是完整 URL 或相对路径）
        params: 请求参数字典
        method: HTTP 方法，默认为 GET
        username: 可选的 GitHub 用户名，会添加到请求头中
    
    Returns:
        包含响应数据和状态的字典:
        {
            "success": bool,
            "data": dict/list,  # 成功时的响应数据
            "error": str,       # 失败时的错误信息
            "status_code": int  # HTTP 状态码
        }
    
    Raises:
        aiohttp.ClientError: 网络请求异常
    """
    # 如果 URL 不是完整 URL，则拼接 GitHub API 基础 URL
    if not url.startswith("http"):
        url = f"{GITHUB_API_BASE}{url}" if url.startswith("/") else f"{GITHUB_API_BASE}/{url}"
    
    # 每次请求都创建新的 session，避免事件循环问题
    # 使用 context manager 确保正确清理
    async with aiohttp.ClientSession() as session:
        try:
            async with session.request(
                method=method,
                url=url,
                headers=get_headers(username=username),
                params=params or {}
            ) as response:
                # 尝试解析 JSON 响应
                try:
                    response_data = await response.json()
                except aiohttp.ContentTypeError:
                    response_text = await response.text()
                    response_data = {"raw": response_text}
                
                # 检查 HTTP 状态码
                if response.status >= 400:
                    error_msg = response_data.get("message", f"HTTP {response.status} 错误")
                    return {
                        "success": False,
                        "error": error_msg,
                        "status_code": response.status,
                        "data": None
                    }
                
                return {
                    "success": True,
                    "data": response_data,
                    "status_code": response.status,
                    "error": None
                }
        
        except aiohttp.ClientError as e:
            return {
                "success": False,
                "error": f"请求异常: {str(e)}",
                "status_code": 500,
                "data": None
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"未知错误: {str(e)}",
                "status_code": 500,
                "data": None
            }


async def search_repository_by_url(repo_url: str, per_page: int = 30, page: int = 1, sort: str = "stars", order: str = "desc") -> Dict:
    """
    通过仓库地址模糊查找仓库信息
    
    Args:
        repo_url: 仓库地址，支持以下格式：
            - 完整 URL: https://github.com/owner/repo
            - GitHub URL: github.com/owner/repo
            - 简短格式: owner/repo
            - 仓库名称: repo (会进行模糊搜索)
        per_page: 每页返回数量，默认 30
        page: 页码，默认 1
        sort: 排序方式，可选值: stars, forks, updated, 默认 stars
        order: 排序顺序，可选值: desc, asc, 默认 desc
    
    Returns:
        包含搜索结果和状态的字典:
        {
            "success": bool,
            "data": {
                "search_keyword": str,      # 搜索关键词
                "total_count": int,          # 总匹配数
                "returned_count": int,       # 返回数量
                "repositories": list         # 仓库列表
            },
            "error": str,
            "status_code": int
        }
    """
    # 解析仓库地址
    search_keyword = repo_url.strip()
    
    # 如果是完整 URL，提取 owner/repo
    if "github.com" in search_keyword:
        # 处理 https://github.com/owner/repo 或 github.com/owner/repo
        parts = search_keyword.replace("https://", "").replace("http://", "").split("/")
        if len(parts) >= 3:
            # 提取 owner/repo
            owner = parts[1]
            repo = parts[2].split("?")[0].split("#")[0]  # 移除查询参数和锚点
            search_keyword = f"{owner}/{repo}"
        elif len(parts) == 2:
            # 只有 owner/repo
            search_keyword = "/".join(parts[1:])
    
    # 判断是精确查询还是模糊搜索
    if "/" in search_keyword:
        # 有斜杠，可能是 owner/repo 格式，先尝试精确查询
        parts = search_keyword.split("/")
        if len(parts) == 2:
            owner, repo_name = parts
            # 先尝试精确查询
            exact_result = await github_api_request(f"/repos/{owner}/{repo_name}", username=owner)
            if exact_result["success"]:
                # 精确匹配成功，返回单个仓库
                repo_data = exact_result["data"]
                formatted_repo = {
                    "id": repo_data["id"],
                    "name": repo_data["name"],
                    "full_name": repo_data["full_name"],
                    "description": repo_data.get("description"),
                    "url": repo_data["html_url"],
                    "language": repo_data.get("language"),
                    "stars": repo_data["stargazers_count"],
                    "forks": repo_data["forks_count"],
                    "watchers": repo_data["watchers_count"],
                    "open_issues": repo_data["open_issues_count"],
                    "default_branch": repo_data["default_branch"],
                    "created_at": repo_data["created_at"],
                    "updated_at": repo_data["updated_at"],
                    "pushed_at": repo_data.get("pushed_at"),
                    "is_private": repo_data["private"],
                    "is_fork": repo_data["fork"],
                    "topics": repo_data.get("topics", []),
                    "license": repo_data.get("license"),
                    "owner": {
                        "login": repo_data["owner"]["login"],
                        "avatar_url": repo_data["owner"]["avatar_url"],
                        "type": repo_data["owner"]["type"]
                    }
                }
                return {
                    "success": True,
                    "data": {
                        "search_keyword": search_keyword,
                        "total_count": 1,
                        "returned_count": 1,
                        "repositories": [formatted_repo]
                    },
                    "error": None,
                    "status_code": 200
                }
    
    # 模糊搜索模式：使用 GitHub Search API
    # 构建搜索查询：在仓库名称中搜索关键词，并限制为指定用户的仓库
    if GITHUB_USERNAME:
        # 如果设置了 GITHUB_USERNAME，只搜索该用户的仓库
        search_query = f"{search_keyword} in:name user:{GITHUB_USERNAME}"
    else:
        # 如果没有设置 GITHUB_USERNAME，进行全局搜索
        search_query = f"{search_keyword} in:name"
    
    params = {
        "q": search_query,
        "per_page": per_page,
        "page": page,
        "sort": sort,
        "order": order
    }
    
    result = await github_api_request("/search/repositories", params=params)
    
    if not result["success"]:
        return result
    
    search_data = result["data"]
    repos = search_data.get("items", [])
    
    formatted_repos = [
        {
            "id": repo["id"],
            "name": repo["name"],
            "full_name": repo["full_name"],
            "description": repo.get("description"),
            "url": repo["html_url"],
            "language": repo.get("language"),
            "stars": repo["stargazers_count"],
            "forks": repo["forks_count"],
            "watchers": repo["watchers_count"],
            "open_issues": repo["open_issues_count"],
            "default_branch": repo.get("default_branch"),
            "created_at": repo["created_at"],
            "updated_at": repo["updated_at"],
            "pushed_at": repo.get("pushed_at"),
            "is_private": repo["private"],
            "is_fork": repo["fork"],
            "topics": repo.get("topics", []),
            "license": repo.get("license"),
            "owner": {
                "login": repo["owner"]["login"],
                "avatar_url": repo["owner"]["avatar_url"],
                "type": repo["owner"]["type"]
            }
        }
        for repo in repos
    ]
    
    return {
        "success": True,
        "data": {
            "search_keyword": search_keyword,
            "total_count": search_data.get("total_count", 0),
            "returned_count": len(formatted_repos),
            "repositories": formatted_repos
        },
        "error": None,
        "status_code": 200
    }


async def get_pull_requests_by_repo_id(repo_id: int, state: str = "open", per_page: int = 30, page: int = 1, sort: str = "created", direction: str = "desc") -> Dict:
    """
    根据仓库 ID 获取该仓库的所有 Pull Requests
    
    Args:
        repo_id: 仓库 ID（整数）
        state: PR 状态，可选值: open, closed, all，默认 open
        per_page: 每页返回数量，默认 30
        page: 页码，默认 1
        sort: 排序方式，可选值: created, updated, popularity，默认 created
        direction: 排序顺序，可选值: asc, desc，默认 desc
    
    Returns:
        包含 Pull Requests 数据和状态的字典:
        {
            "success": bool,
            "data": {
                "repository_id": int,        # 仓库 ID
                "state": str,                 # PR 状态
                "total": int,                 # 返回的 PR 数量
                "pull_requests": [           # Pull Requests 列表
                    {
                        "number": int,
                        "title": str,
                        "body": str,
                        "state": str,
                        "url": str,
                        "user": dict,
                        "created_at": str,
                        "updated_at": str,
                        "merged_at": str,
                        "mergeable": bool,
                        "draft": bool,
                        "head": dict,
                        "base": dict
                    }
                ]
            },
            "error": str,
            "status_code": int
        }
    """
    params = {
        "state": state,
        "per_page": per_page,
        "page": page,
        "sort": sort,
        "direction": direction
    }
    
    # 使用仓库 ID 查询 Pull Requests
    result = await github_api_request(f"/repositories/{repo_id}/pulls", params=params)
    
    if not result["success"]:
        if result["status_code"] == 404:
            return {
                "success": False,
                "error": f"仓库 ID {repo_id} 不存在或无权访问",
                "status_code": 404,
                "data": None
            }
        return result
    
    pulls = result["data"]
    
    formatted_pulls = [
        {
            "number": pr["number"],
            "title": pr["title"],
            "body": pr.get("body", ""),
            "state": pr["state"],
            "url": pr["html_url"],
            "user": {
                "login": pr["user"]["login"],
                "avatar_url": pr["user"]["avatar_url"],
                "type": pr["user"].get("type", "User")
            },
            "created_at": pr["created_at"],
            "updated_at": pr["updated_at"],
            "merged_at": pr.get("merged_at"),
            "mergeable": pr.get("mergeable"),
            "merged": pr.get("merged", False),
            "draft": pr.get("draft", False),
            "additions": pr.get("additions"),
            "deletions": pr.get("deletions"),
            "changed_files": pr.get("changed_files"),
            "commits": pr.get("commits", 0),
            "head": {
                "ref": pr["head"]["ref"],
                "sha": pr["head"]["sha"],
                "repo": pr["head"]["repo"]["full_name"] if pr["head"].get("repo") else None
            },
            "base": {
                "ref": pr["base"]["ref"],
                "sha": pr["base"]["sha"],
                "repo": pr["base"]["repo"]["full_name"] if pr["base"].get("repo") else None
            }
        }
        for pr in pulls
    ]
    
    return {
        "success": True,
        "data": {
            "repository_id": repo_id,
            "state": state,
            "total": len(formatted_pulls),
            "pull_requests": formatted_pulls
        },
        "error": None,
        "status_code": 200
    }


async def get_pull_request_files_by_repo_id(repo_id: int, pr_number: int) -> Dict:
    """
    根据仓库 ID 和 Pull Request 编号获取变更文件和变更内容
    
    Args:
        repo_id: 仓库 ID（整数）
        pr_number: Pull Request 编号（整数）
    
    Returns:
        包含变更文件数据和状态的字典:
        {
            "success": bool,
            "data": {
                "repository_id": int,        # 仓库 ID
                "pull_request_number": int,  # PR 编号
                "total_files": int,          # 变更文件总数
                "total_additions": int,       # 总添加行数
                "total_deletions": int,       # 总删除行数
                "total_changes": int,         # 总变更行数
                "files": [                   # 变更文件列表
                    {
                        "filename": str,
                        "status": str,        # added, removed, modified, renamed, copied, changed, unchanged
                        "additions": int,
                        "deletions": int,
                        "changes": int,
                        "patch": str,         # 变更内容的补丁（diff）
                        "previous_filename": str,  # 重命名前的文件名
                        "blob_url": str,
                        "raw_url": str,
                        "contents_url": str
                    }
                ]
            },
            "error": str,
            "status_code": int
        }
    """
    # 使用仓库 ID 和 PR 编号查询文件变更
    result = await github_api_request(f"/repositories/{repo_id}/pulls/{pr_number}/files")
    
    if not result["success"]:
        if result["status_code"] == 404:
            return {
                "success": False,
                "error": f"仓库 ID {repo_id} 的 Pull Request #{pr_number} 不存在或无权访问",
                "status_code": 404,
                "data": None
            }
        return result
    
    files = result["data"]
    
    # 计算总计
    total_additions = sum(file.get("additions", 0) for file in files)
    total_deletions = sum(file.get("deletions", 0) for file in files)
    total_changes = sum(file.get("changes", 0) for file in files)
    
    formatted_files = [
        {
            "filename": file["filename"],
            "status": file["status"],  # added, removed, modified, renamed, copied, changed, unchanged
            "additions": file.get("additions", 0),
            "deletions": file.get("deletions", 0),
            "changes": file.get("changes", 0),
            "patch": file.get("patch", ""),  # 变更内容的补丁（diff格式）
            "previous_filename": file.get("previous_filename"),  # 重命名前的文件名
            "blob_url": file.get("blob_url", ""),
            "raw_url": file.get("raw_url", ""),
            "contents_url": file.get("contents_url", "")
        }
        for file in files
    ]
    
    return {
        "success": True,
        "data": {
            "repository_id": repo_id,
            "pull_request_number": pr_number,
            "total_files": len(formatted_files),
            "total_additions": total_additions,
            "total_deletions": total_deletions,
            "total_changes": total_changes,
            "files": formatted_files
        },
        "error": None,
        "status_code": 200
    }