# Foreign Trade News Collector v3
# Raw data collection only, grouping done in JS

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$OutputFile = "C:\Users\12728\.qclaw\workspace\news-archive\data.json"

# Load API Key
$ApiKey = $env:TAVILY_API_KEY
if (-not $ApiKey) {
    $envPath = Join-Path $env:USERPROFILE ".openclaw\.env"
    if (Test-Path $envPath) {
        $content = Get-Content $envPath -Raw -Encoding UTF8
        if ($content -match "TAVILY_API_KEY\s*=\s*(.+)") {
            $ApiKey = $Matches[1].Trim().Trim('"').Trim("'")
        }
    }
}

if (-not $ApiKey) {
    Write-Error "Missing TAVILY_API_KEY"
    exit 1
}

# Topics with category IDs
$topics = @(
    @{ q = "China tariff policy export rebate 2026"; cat = "tariff" },
    @{ q = "China foreign trade data statistics 2026"; cat = "data" },
    @{ q = "China US trade negotiation geopolitics 2026"; cat = "geo" },
    @{ q = "RMB yuan exchange rate dollar 2026"; cat = "fx" },
    @{ q = "China port logistics shipping freight 2026"; cat = "logistics" }
)

$now = Get-Date
$newsList = @()

foreach ($topic in $topics) {
    Write-Host "Searching: $($topic.q)" -ForegroundColor Cyan
    
    $body = @{
        api_key = $ApiKey
        query = $topic.q
        max_results = 3
        search_depth = "basic"
        include_answer = $false
        include_images = $false
        include_raw_content = $false
    } | ConvertTo-Json

    try {
        $response = Invoke-RestMethod -Uri "https://api.tavily.com/search" -Method POST -Body $body -Headers @{"Content-Type"="application/json"} -TimeoutSec 30
        
        $count = 0
        foreach ($result in $response.results) {
            if ($count -ge 2) { break }
            
            $impact = "medium"
            $content = $result.content + $result.title
            if ($content -match "high|critical|crisis|tariff ban|100%|prohibit|zero") {
                $impact = "high"
            }
            
            $source = "web"
            if ($result.url -match "//([^/]+)") {
                $source = $Matches[1] -replace "^www\.", ""
            }
            
            $item = [ordered]@{
                id = $now.ToString("yyyyMMdd") + "-" + [guid]::NewGuid().ToString("N").Substring(0,6)
                title = $result.title
                source = $source
                category = $topic.cat
                impact = $impact
                snippet = $result.content
                url = $result.url
                timestamp = $now.ToString("yyyy-MM-ddTHH:mm:ss+08:00")
            }
            
            $newsList += $item
            $count++
        }
        
        Write-Host "  + $count items" -ForegroundColor Green
    } catch {
        Write-Warning "Search failed: $_"
    }
    
    Start-Sleep -Milliseconds 500
}

# Build final data (no grouping - JS will handle it)
$data = [ordered]@{
    dateShort = $now.ToString("yyyy-MM-dd")
    generatedAt = $now.ToString("HH:mm")
    news = $newsList
    stats = [ordered]@{
        totalNews = $newsList.Count
    }
}

# Save
$json = $data | ConvertTo-Json -Depth 10
[System.IO.File]::WriteAllText($OutputFile, $json, [System.Text.Encoding]::UTF8)

Write-Host ""
Write-Host "Done. Saved $($newsList.Count) news items" -ForegroundColor Yellow
