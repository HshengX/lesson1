# Cursor MCP Configuration Script (PowerShell)
# Add gitcode MCP server to Cursor

$cursorConfigDir = "$env:APPDATA\Cursor\User"
$mcpConfigFile = "$cursorConfigDir\mcp.json"
$projectPath = "D:\ai\aiproject\gf-aiproject\gfMcpCourse\lesson1"
$gitcodeScript = "$projectPath\src\mcp\gitcode_mcp.py"

# Create config directory if it doesn't exist
if (-not (Test-Path $cursorConfigDir)) {
    New-Item -ItemType Directory -Path $cursorConfigDir -Force | Out-Null
    Write-Host "Created Cursor config directory: $cursorConfigDir" -ForegroundColor Green
}

# Read existing config if it exists
$config = @{}
if (Test-Path $mcpConfigFile) {
    try {
        $content = Get-Content $mcpConfigFile -Raw -Encoding UTF8
        $config = $content | ConvertFrom-Json
        Write-Host "Read existing MCP config" -ForegroundColor Yellow
    } catch {
        Write-Host "Could not read existing config, will create new one" -ForegroundColor Yellow
        $config = New-Object PSObject
    }
}

# Ensure mcpServers object exists
if (-not $config.mcpServers) {
    $config | Add-Member -MemberType NoteProperty -Name "mcpServers" -Value (New-Object PSObject) -Force
}

# Create gitcode server config
$gitcodeConfig = New-Object PSObject
$gitcodeConfig | Add-Member -MemberType NoteProperty -Name "command" -Value "python"
$gitcodeConfig | Add-Member -MemberType NoteProperty -Name "args" -Value @($gitcodeScript)
$envConfig = New-Object PSObject
$envConfig | Add-Member -MemberType NoteProperty -Name "GITHUB_TOKEN" -Value ""
$envConfig | Add-Member -MemberType NoteProperty -Name "GITHUB_USERNAME" -Value ""
$gitcodeConfig | Add-Member -MemberType NoteProperty -Name "env" -Value $envConfig

# Add or update gitcode in mcpServers
$config.mcpServers | Add-Member -MemberType NoteProperty -Name "gitcode" -Value $gitcodeConfig -Force

# Convert to JSON and save
$json = $config | ConvertTo-Json -Depth 10
$json | Set-Content $mcpConfigFile -Encoding UTF8

Write-Host ""
Write-Host "MCP config saved to: $mcpConfigFile" -ForegroundColor Green
Write-Host ""
Write-Host "Configuration content:" -ForegroundColor Cyan
Get-Content $mcpConfigFile | Write-Host
Write-Host ""
Write-Host "Please edit the config file to fill in GITHUB_TOKEN and GITHUB_USERNAME if needed" -ForegroundColor Yellow
Write-Host "Or make sure environment variables are set." -ForegroundColor Yellow
Write-Host ""
Write-Host "After configuration, please restart Cursor for the changes to take effect." -ForegroundColor Green
