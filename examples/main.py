import asyncio
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.github.server import search_repository_by_url, get_pull_requests_by_repo_id, get_pull_request_files_by_repo_id

async def main():
    # 1. 搜索仓库获取 ID
    repo_result = await search_repository_by_url("lesson")
    if not repo_result["success"]:
        print(f"错误: {repo_result['error']}")
        return
    
    repo_id = repo_result["data"]["repositories"][0]["id"]
    print(f"仓库 ID: {repo_id}")
    
    # 2. 获取该仓库的 Pull Requests
    prs_result = await get_pull_requests_by_repo_id(repo_id, state="open")
    if not prs_result["success"]:
        print(f"错误: {prs_result['error']}")
        return
    
    # 3. 获取第一个 PR 的变更文件
    if prs_result["data"]["pull_requests"]:
        first_pr = prs_result["data"]["pull_requests"][0]
        pr_number = first_pr["number"]
        
        files_result = await get_pull_request_files_by_repo_id(repo_id, pr_number)
        if files_result["success"]:
            print(f"PR #{pr_number} 的变更文件:")
            for file in files_result["data"]["files"]:
                print(f"  {file['filename']}: +{file['additions']} -{file['deletions']}")

asyncio.run(main())