$ErrorActionPreference = "Stop"

# ===========================================================
# PLAYLIST HUB - SYNC SCRIPT (Cap Toc 2026)
# Toan Ca Chep - 2026
# ===========================================================

$CsvPath = ".\quan_ly_de_thi.csv"
$KhoDeGoc = ".\01_Kho_De_Goc"
$TestWebDir = "..\Test_Web"
$DestDeDir = ".\de"
$HtmlPath = ".\index.html"

# ============== PHASE 0: AUTO-DISCOVERY ==============
Write-Host ""
Write-Host "=========================================" -ForegroundColor Magenta
Write-Host "  ROBOT CAP TOC 2026 (Auto-Discovery)" -ForegroundColor Magenta
Write-Host "=========================================" -ForegroundColor Magenta

# Dam bao thu muc 01_Kho_De_Goc ton tai
if (-not (Test-Path $KhoDeGoc)) {
    New-Item -ItemType Directory -Path $KhoDeGoc -Force | Out-Null
}

# Doc CSV hien tai
$csvExists = Test-Path $CsvPath
if ($csvExists) {
    $csvContent = Get-Content $CsvPath -Raw -Encoding UTF8
    if ([string]::IsNullOrWhiteSpace($csvContent) -or $csvContent.Trim().Split("`n").Count -le 1) {
        $csvData = @()
    } else {
        $csvData = Import-Csv $CsvPath -Encoding UTF8
    }
} else {
    $csvData = @()
    # Tao CSV voi header
    "ID,Ten_De,Loai,Buoi,So_Cau,Thoi_Gian,File_Goc,Trang_Thai,Mat_Khau" | Set-Content $CsvPath -Encoding UTF8
}

# Lay danh sach File_Goc da co trong CSV
$existingFiles = @()
foreach ($row in $csvData) {
    $existingFiles += $row.File_Goc
}

# Tim so ID lon nhat hien tai
$maxIdNum = 0
foreach ($row in $csvData) {
    if ($row.ID -match 'ld_(\d+)') {
        $num = [int]$Matches[1]
        if ($num -gt $maxIdNum) { $maxIdNum = $num }
    }
}

# ============== QUET FILE MOI TU KHO ==============
Write-Host ""
Write-Host "Dang quet 01_Kho_De_Goc..." -ForegroundColor Cyan

# Quet cac file LD*.html trong 01_Kho_De_Goc
$khoFiles = Get-ChildItem -Path $KhoDeGoc -Filter "LD*.html" -File -ErrorAction SilentlyContinue
$newEntriesAdded = $false

foreach ($file in $khoFiles) {
    $shortName = $file.Name
    $alreadyInCsv = $existingFiles -contains $shortName

    if ($alreadyInCsv) {
        Write-Host " Da co: $shortName" -ForegroundColor DarkGray
        continue
    }

    # Parse ten file: LD01.html -> so 01
    if ($shortName -match 'LD(\d{2})\.html') {
        $soDe = [int]$Matches[1]
    } else {
        Write-Host " Khong doc duoc: $shortName -> Bo qua" -ForegroundColor DarkGray
        continue
    }

    $maxIdNum++
    $newId = "ld_{0:D2}" -f $soDe

    # Le = tren_lop, Chan = ve_nha
    if ($soDe % 2 -eq 1) {
        $loai = "tren_lop"
        $thoiGian = 90
    } else {
        $loai = "ve_nha"
        $thoiGian = 0
    }

    # Tinh buoi: LD01-02 = B1, LD03-04 = B2, ...
    $buoi = [Math]::Ceiling($soDe / 2)

    # Dem so cau tu file HTML
    $htmlRaw = Get-Content $file.FullName -Raw -Encoding UTF8
    $slideCount = ([regex]::Matches($htmlRaw, 'class="slide"')).Count
    $soCau = [Math]::Max($slideCount - 2, 0)
    if ($soCau -eq 0) { $soCau = 22 } # default

    $tenDe = "LD{0:D2}" -f $soDe
    $newLine = "$newId,$tenDe,$loai,$buoi,$soCau,$thoiGian,$shortName,Hien,"
    Add-Content -Path $CsvPath -Value $newLine -Encoding UTF8
    $newEntriesAdded = $true
    $existingFiles += $shortName

    $loaiDisplay = if ($loai -eq "tren_lop") { "Tren lop" } else { "Ve nha" }
    Write-Host " MOI: $tenDe -> $newId (Buoi $buoi, $loaiDisplay, $soCau cau)" -ForegroundColor Green
}

# Quet them tu Test_Web neu co thu muc LD
Write-Host ""
Write-Host "Dang quet Test_Web..." -ForegroundColor Cyan
if (Test-Path $TestWebDir) {
    $testWebFolders = Get-ChildItem -Path $TestWebDir -Directory | Where-Object { $_.Name -match '^\d{8}_LD' }
    foreach ($folder in $testWebFolders) {
        $outputDir = Join-Path $folder.FullName "03_Outputs"
        if (-not (Test-Path $outputDir)) { continue }

        $htmlFiles = Get-ChildItem -Path $outputDir -Filter "LD*.html" -File
        foreach ($htmlFile in $htmlFiles) {
            $shortName = $htmlFile.Name
            if ($existingFiles -contains $shortName) {
                # Kiem tra cap nhat
                $khoDestPath = Join-Path $KhoDeGoc $shortName
                if (Test-Path $khoDestPath) {
                    $sourceTime = $htmlFile.LastWriteTime
                    $destTime = (Get-Item $khoDestPath).LastWriteTime
                    if ($sourceTime -gt $destTime) {
                        Copy-Item -Path $htmlFile.FullName -Destination $khoDestPath -Force
                        Write-Host " CAP NHAT: $shortName" -ForegroundColor Yellow
                    }
                }
                continue
            }

            # File moi -> copy vao Kho
            $khoDestPath = Join-Path $KhoDeGoc $shortName
            Copy-Item -Path $htmlFile.FullName -Destination $khoDestPath -Force
            Write-Host " COPY TU TEST_WEB: $shortName" -ForegroundColor Green

            # Parse va them CSV (se duoc xu ly vong lap ke tiep)
        }
    }

    # Re-scan Kho sau khi copy tu Test_Web
    $khoFiles2 = Get-ChildItem -Path $KhoDeGoc -Filter "LD*.html" -File -ErrorAction SilentlyContinue
    foreach ($file in $khoFiles2) {
        $shortName = $file.Name
        if ($existingFiles -contains $shortName) { continue }

        if ($shortName -match 'LD(\d{2})\.html') {
            $soDe = [int]$Matches[1]
        } else { continue }

        $newId = "ld_{0:D2}" -f $soDe
        $loai = if ($soDe % 2 -eq 1) { "tren_lop" } else { "ve_nha" }
        $thoiGian = if ($soDe % 2 -eq 1) { 90 } else { 0 }
        $buoi = [Math]::Ceiling($soDe / 2)

        $htmlRaw = Get-Content $file.FullName -Raw -Encoding UTF8
        $slideCount = ([regex]::Matches($htmlRaw, 'class="slide"')).Count
        $soCau = [Math]::Max($slideCount - 2, 0)
        if ($soCau -eq 0) { $soCau = 22 }

        $tenDe = "LD{0:D2}" -f $soDe
        $newLine = "$newId,$tenDe,$loai,$buoi,$soCau,$thoiGian,$shortName,Hien,"
        Add-Content -Path $CsvPath -Value $newLine -Encoding UTF8
        $newEntriesAdded = $true
        $existingFiles += $shortName
        Write-Host " MOI (tu Test_Web): $tenDe" -ForegroundColor Green
    }
} else {
    Write-Host " Thu muc Test_Web khong ton tai, bo qua." -ForegroundColor DarkGray
}

# Reload CSV
if ($newEntriesAdded) {
    Write-Host ""
    Write-Host "Da tu dong them de moi vao CSV!" -ForegroundColor Green
}

$csvContent = Get-Content $CsvPath -Raw -Encoding UTF8
if ([string]::IsNullOrWhiteSpace($csvContent) -or $csvContent.Trim().Split("`n").Count -le 1) {
    $csvData = @()
} else {
    $csvData = Import-Csv $CsvPath -Encoding UTF8
}

# ============== PHASE 1: BUILD ==============
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  BUILD" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

Write-Host ""
Write-Host "1. Don dep thu muc 'de'..." -ForegroundColor Cyan
if (Test-Path $DestDeDir) {
    Remove-Item -Path "$DestDeDir\*" -Recurse -Force
}
else {
    New-Item -ItemType Directory -Path $DestDeDir -Force | Out-Null
}

$examsJsonArr = @()

Write-Host "2. Xu ly va copy de thi..." -ForegroundColor Cyan
foreach ($row in $csvData) {
    if ($row.Trang_Thai -ne "Hien") {
        Write-Host " Bo qua (AN): $($row.Ten_De)" -ForegroundColor DarkGray
        continue
    }

    $sourcePath = Join-Path $KhoDeGoc $row.File_Goc
    if (-not (Test-Path $sourcePath)) {
        Write-Host " LOI: Khong tim thay file $($row.File_Goc)" -ForegroundColor Red
        continue
    }

    $destFileName = ""
    $hasPassword = "false"
    $fileVal = "null"

    if ([string]::IsNullOrWhiteSpace($row.Mat_Khau)) {
        # Khong co mat khau (truong hop hiem)
        $destFileName = "$($row.ID).html"
        $fileVal = "'de/$destFileName'"
        Write-Host " OK: $($row.Ten_De) -> $destFileName" -ForegroundColor Green
    }
    else {
        # Co mat khau -> hash SHA-256
        $bytes = [System.Text.Encoding]::UTF8.GetBytes($row.Mat_Khau)
        $hashBytes = [System.Security.Cryptography.SHA256]::Create().ComputeHash($bytes)
        $hashString = [System.BitConverter]::ToString($hashBytes).Replace('-', '').ToLower()
        $destFileName = "de_$hashString.html"
        $hasPassword = "true"
        Write-Host " OK (MAT KHAU): $($row.Ten_De) -> Ma hoa" -ForegroundColor Yellow
    }

    $destPath = Join-Path $DestDeDir $destFileName
    Copy-Item -Path $sourcePath -Destination $destPath -Force

    # Icon: lay so de
    $icon = $row.Ten_De
    if ($row.Ten_De -match '(\d{2})') {
        $icon = $Matches[1]
    }

    # Icon style: tren_lop = blue, ve_nha = orange
    $iconStyle = "blue"
    if ($row.Loai -eq "ve_nha") {
        $iconStyle = "orange"
    }

    $jsonObj = @"
  {
    id: '$($row.ID)',
    file: $fileVal,
    hasPassword: $hasPassword,
    title: '$($row.Ten_De)',
    loai: '$($row.Loai)',
    buoi: $($row.Buoi),
    questions: $($row.So_Cau),
    duration: $($row.Thoi_Gian),
    icon: '$icon',
    iconStyle: '$iconStyle'
  }
"@
    $examsJsonArr += $jsonObj
}

Write-Host "3. Cap nhat index.html..." -ForegroundColor Cyan
$examsJsonStr = $examsJsonArr -join ",`n"
$htmlContent = Get-Content $HtmlPath -Raw -Encoding UTF8
$pattern = "(?s)const EXAMS = \[.*?\];"
$replacement = "const EXAMS = [`n$examsJsonStr`n];"
$newHtmlContent = $htmlContent -replace $pattern, $replacement
Set-Content -Path $HtmlPath -Value $newHtmlContent -Encoding UTF8

# ============== PHASE 2: GITHUB PUSH ==============
Write-Host ""
Write-Host "4. Dong bo len GitHub..." -ForegroundColor Cyan
if (-not (Test-Path ".git")) {
    Write-Host " Khoi tao Git..." -ForegroundColor DarkGray
    git init
    git branch -M main
}

git add .
git commit -m "Auto-sync Cap Toc 2026 $(Get-Date -Format 'yyyy-MM-dd HH:mm')"

$remote = git remote -v
if (-not $remote) {
    Write-Host " CHUA CAU HINH GITHUB REMOTE." -ForegroundColor Red
    Write-Host " Chay lenh sau de them remote:" -ForegroundColor Yellow
    Write-Host "   git remote add origin https://github.com/LopToanCaChep/captoc-2026.git" -ForegroundColor White
}
else {
    Write-Host " Dang day len GitHub..." -ForegroundColor Yellow
    git push -u origin main
    Write-Host ""
    Write-Host "=========================================" -ForegroundColor Green
    Write-Host "  HOAN TAT! DA DAY LEN GITHUB THANH CONG" -ForegroundColor Green
    Write-Host "=========================================" -ForegroundColor Green
}

Write-Host ""
