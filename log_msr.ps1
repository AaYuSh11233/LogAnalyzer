# Log Monitor and Measurement Script
# This script monitors log files in a directory and provides basic statistics

param(
    [string]$LogDirectory = "logs",
    [int]$RefreshInterval = 30
)

Write-Host "📊 Log Monitor & Measurement Tool" -ForegroundColor Green
Write-Host "Monitoring directory: $LogDirectory" -ForegroundColor Yellow
Write-Host "Refresh interval: $RefreshInterval seconds" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop monitoring" -ForegroundColor Red
Write-Host ""

try {
    while ($true) {
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        Write-Host "[$timestamp] Scanning for log files..." -ForegroundColor Cyan
        
        if (Test-Path $LogDirectory) {
            $logFiles = Get-ChildItem -Path $LogDirectory -Filter "*.log" -Recurse
            $csvFiles = Get-ChildItem -Path $LogDirectory -Filter "*.csv" -Recurse
            $jsonFiles = Get-ChildItem -Path $LogDirectory -Filter "*.json" -Recurse
            
            $totalFiles = $logFiles.Count + $csvFiles.Count + $jsonFiles.Count
            
            if ($totalFiles -gt 0) {
                Write-Host "Found $totalFiles log files:" -ForegroundColor Green
                Write-Host "  - Log files: $($logFiles.Count)" -ForegroundColor White
                Write-Host "  - CSV files: $($csvFiles.Count)" -ForegroundColor White
                Write-Host "  - JSON files: $($jsonFiles.Count)" -ForegroundColor White
                
                $totalSize = 0
                foreach ($file in @($logFiles, $csvFiles, $jsonFiles)) {
                    $totalSize += $file.Length
                }
                Write-Host "Total size: $([math]::Round($totalSize/1KB, 2)) KB" -ForegroundColor Yellow
            } else {
                Write-Host "No log files found in $LogDirectory" -ForegroundColor Yellow
            }
        } else {
            Write-Host "Directory $LogDirectory does not exist" -ForegroundColor Red
        }
        
        Write-Host ""
        Start-Sleep -Seconds $RefreshInterval
    }
} catch {
    Write-Host "`nMonitoring stopped." -ForegroundColor Red
}
