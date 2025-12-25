"""
GitHub API 工具定义（遵循 OpenAI Function Calling 规范）
提供 search_repository_by_url, get_pull_requests_by_repo_id, get_pull_request_files_by_repo_id 三个工具
"""
from typing import Dict, List, Any
import asyncio
from server import (
    search_repository_by_url,
    get_pull_requests_by_repo_id,
    get_pull_request_files_by_repo_id,
    get_commits_by_repo_id
)


def get_github_tools() -> List[Dict[str, Any]]:
    """
    获取 GitHub API 工具定义（符合 OpenAI Function Calling 规范）
    
    Returns:
        工具定义列表，可以直接传递给 OpenAI API 的 tools 参数
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "search_repository_by_url",
                "description": "搜索GitHub仓库。当用户询问仓库信息、查找仓库、需要仓库ID时使用此工具。支持完整URL、简短格式(owner/repo)或仓库名称进行搜索。如果设置了GITHUB_USERNAME，模糊搜索时只搜索该用户的仓库。返回的仓库信息包含仓库ID，可用于后续查询。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "repo_url": {
                            "type": "string",
                            "description": "仓库地址，支持以下格式：1) 完整URL: https://github.com/owner/repo, 2) GitHub URL: github.com/owner/repo, 3) 简短格式: owner/repo, 4) 仓库名称: repo (会进行模糊搜索)"
                        },
                        "per_page": {
                            "type": "integer",
                            "description": "每页返回数量，默认30",
                            "default": 30,
                            "minimum": 1,
                            "maximum": 100
                        },
                        "page": {
                            "type": "integer",
                            "description": "页码，默认1",
                            "default": 1,
                            "minimum": 1
                        },
                        "sort": {
                            "type": "string",
                            "description": "排序方式",
                            "enum": ["stars", "forks", "updated"],
                            "default": "stars"
                        },
                        "order": {
                            "type": "string",
                            "description": "排序顺序",
                            "enum": ["desc", "asc"],
                            "default": "desc"
                        }
                    },
                    "required": ["repo_url"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_pull_requests_by_repo_id",
                "description": "获取GitHub仓库的Pull Requests（PR）。当用户询问PR、合并请求、拉取请求时使用此工具。需要先通过search_repository_by_url获取仓库ID。可以按状态(open/closed/all)、排序方式等筛选和排序。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "repo_id": {
                            "type": "integer",
                            "description": "仓库ID（整数）"
                        },
                        "state": {
                            "type": "string",
                            "description": "PR状态筛选",
                            "enum": ["open", "closed", "all"],
                            "default": "open"
                        },
                        "per_page": {
                            "type": "integer",
                            "description": "每页返回数量，默认30",
                            "default": 30,
                            "minimum": 1,
                            "maximum": 100
                        },
                        "page": {
                            "type": "integer",
                            "description": "页码，默认1",
                            "default": 1,
                            "minimum": 1
                        },
                        "sort": {
                            "type": "string",
                            "description": "排序方式",
                            "enum": ["created", "updated", "popularity"],
                            "default": "created"
                        },
                        "direction": {
                            "type": "string",
                            "description": "排序顺序",
                            "enum": ["asc", "desc"],
                            "default": "desc"
                        }
                    },
                    "required": ["repo_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_pull_request_files_by_repo_id",
                "description": "获取GitHub Pull Request的变更文件。当用户询问PR的变更内容、修改的文件、diff时使用此工具。需要仓库ID和PR编号。返回文件列表、变更统计和每个文件的diff补丁。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "repo_id": {
                            "type": "integer",
                            "description": "仓库ID（整数）"
                        },
                        "pr_number": {
                            "type": "integer",
                            "description": "Pull Request编号（整数）"
                        }
                    },
                    "required": ["repo_id", "pr_number"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_commits_by_repo_id",
                "description": "获取GitHub仓库的提交历史（commits）。当用户询问提交记录、提交历史、commit历史、代码提交时使用此工具。需要先通过search_repository_by_url获取仓库ID。可以按分支、路径、作者、时间范围等筛选。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "repo_id": {
                            "type": "integer",
                            "description": "仓库ID（整数），可通过search_repository_by_url获取"
                        },
                        "sha": {
                            "type": "string",
                            "description": "分支或提交SHA，默认为默认分支"
                        },
                        "path": {
                            "type": "string",
                            "description": "只返回包含指定路径的提交"
                        },
                        "author": {
                            "type": "string",
                            "description": "只返回指定作者的提交（GitHub用户名或邮箱）"
                        },
                        "since": {
                            "type": "string",
                            "description": "只返回此日期之后的提交（ISO 8601格式，如2024-01-01T00:00:00Z）"
                        },
                        "until": {
                            "type": "string",
                            "description": "只返回此日期之前的提交（ISO 8601格式）"
                        },
                        "per_page": {
                            "type": "integer",
                            "description": "每页返回数量，默认30",
                            "default": 30,
                            "minimum": 1,
                            "maximum": 100
                        },
                        "page": {
                            "type": "integer",
                            "description": "页码，默认1",
                            "default": 1,
                            "minimum": 1
                        }
                    },
                    "required": ["repo_id"]
                }
            }
        }
    ]


# 工具函数映射表
TOOL_FUNCTIONS = {
    "search_repository_by_url": search_repository_by_url,
    "get_pull_requests_by_repo_id": get_pull_requests_by_repo_id,
    "get_pull_request_files_by_repo_id": get_pull_request_files_by_repo_id,
    "get_commits_by_repo_id": get_commits_by_repo_id
}


async def call_tool(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    调用指定的工具函数
    
    Args:
        tool_name: 工具函数名称
        arguments: 函数参数（字典格式）
    
    Returns:
        函数执行结果
    """
    if tool_name not in TOOL_FUNCTIONS:
        return {
            "success": False,
            "error": f"未知的工具函数: {tool_name}",
            "data": None
        }
    
    try:
        func = TOOL_FUNCTIONS[tool_name]
        result = await func(**arguments)
        return result
    except Exception as e:
        return {
            "success": False,
            "error": f"调用工具函数时发生错误: {str(e)}",
            "data": None
        }


def format_tool_result(tool_name: str, result: Dict[str, Any]) -> str:
    """
    将工具执行结果格式化为字符串，便于大模型理解
    
    Args:
        tool_name: 工具函数名称
        result: 函数执行结果
    
    Returns:
        格式化后的字符串
    """
    if not result.get("success"):
        return f"工具调用失败: {result.get('error', '未知错误')}"
    
    data = result.get("data", {})
    
    if tool_name == "search_repository_by_url":
        repos = data.get("repositories", [])
        total = data.get("total_count", 0)
        returned = data.get("returned_count", 0)
        keyword = data.get("search_keyword", "")
        
        if not repos:
            return f"未找到匹配的仓库（搜索关键词: {keyword}）"
        
        summary = f"找到 {total} 个匹配的仓库，返回 {returned} 个：\n\n"
        for i, repo in enumerate(repos[:10], 1):  # 只显示前10个
            summary += f"{i}. {repo['full_name']} (ID: {repo['id']})\n"
            summary += f"   描述: {repo.get('description', '无')}\n"
            summary += f"   语言: {repo.get('language', '未知')}\n"
            summary += f"   Stars: {repo['stars']}, Forks: {repo['forks']}\n"
            summary += f"   URL: {repo['url']}\n\n"
        
        if returned > 10:
            summary += f"... 还有 {returned - 10} 个仓库未显示\n"
        
        return summary
    
    elif tool_name == "get_pull_requests_by_repo_id":
        prs = data.get("pull_requests", [])
        total = data.get("total", 0)
        repo_id = data.get("repository_id", "")
        state = data.get("state", "")
        
        if not prs:
            return f"仓库 ID {repo_id} 没有 {state} 状态的 Pull Requests"
        
        summary = f"仓库 ID {repo_id} 的 {state} 状态 Pull Requests（共 {total} 个）：\n\n"
        for pr in prs[:20]:  # 只显示前20个
            summary += f"PR #{pr['number']}: {pr['title']}\n"
            summary += f"   状态: {pr['state']}, 创建时间: {pr['created_at']}\n"
            summary += f"   作者: {pr['user']['login']}\n"
            summary += f"   URL: {pr['url']}\n"
            if pr.get('merged'):
                summary += f"   已合并于: {pr.get('merged_at', '未知')}\n"
            summary += "\n"
        
        if total > 20:
            summary += f"... 还有 {total - 20} 个 PR 未显示\n"
        
        return summary
    
    elif tool_name == "get_pull_request_files_by_repo_id":
        files = data.get("files", [])
        total_files = data.get("total_files", 0)
        total_additions = data.get("total_additions", 0)
        total_deletions = data.get("total_deletions", 0)
        repo_id = data.get("repository_id", "")
        pr_number = data.get("pull_request_number", "")
        
        if not files:
            return f"PR #{pr_number} 没有变更文件"
        
        summary = f"PR #{pr_number} (仓库 ID: {repo_id}) 的变更文件：\n"
        summary += f"总文件数: {total_files}, 总添加: +{total_additions}, 总删除: -{total_deletions}\n\n"
        
        for file in files[:15]:  # 只显示前15个文件
            summary += f"文件: {file['filename']} ({file['status']})\n"
            summary += f"  变更: +{file['additions']} -{file['deletions']} ({file['changes']} 行)\n"
            if file.get('previous_filename'):
                summary += f"  重命名自: {file['previous_filename']}\n"
            if file.get('patch'):
                # 只显示补丁的前200个字符
                patch_preview = file['patch'][:200].replace('\n', '\\n')
                summary += f"  变更预览: {patch_preview}...\n"
            summary += "\n"
        
        if total_files > 15:
            summary += f"... 还有 {total_files - 15} 个文件未显示\n"
        
        return summary
    
    else:
        # 默认格式化为 JSON
        import json
        return json.dumps(data, ensure_ascii=False, indent=2)

