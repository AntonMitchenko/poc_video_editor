param (
    [string]$input_file,
    [int]$num_clips,
    [string]$clips_dir
)

$filename = [System.IO.Path]::GetFileNameWithoutExtension($input_file)

if (-Not (Test-Path -Path $clips_dir)) {
    New-Item -ItemType Directory -Path $clips_dir
}

$duration_line = & ffmpeg -i $input_file 2>&1 | Select-String "Duration"
Write-Output "Duration line: $duration_line"

if ($duration_line -match "Duration: (\d{2}):(\d{2}):(\d{2})\.(\d{2})") {
    $hours = [int]$matches[1]
    $minutes = [int]$matches[2]
    $seconds = [int]$matches[3]
    $milliseconds = [int]$matches[4]
    $duration_seconds = ($hours * 3600) + ($minutes * 60) + $seconds + ($milliseconds / 100)
    Write-Output "Duration in seconds: $duration_seconds"
} else {
    Write-Output "Failed to parse duration. Duration line was: $duration_line"
    exit 1
}


$clip_duration = $duration_seconds / $num_clips

$output_files = @()

# Цикл для создания клипов
for ($i = 0; $i -lt $num_clips; $i++) {
    $start_time = $i * $clip_duration
    $output_file = "$clips_dir/clip$($i + 1).mp4"
    $output_files += $output_file
    $start_time_str = [TimeSpan]::FromSeconds($start_time).ToString("hh\:mm\:ss")
    Write-Output "Processing clip ${i + 1} of ${num_clips}: ${output_file}"
    & ffmpeg -i $input_file -ss $start_time_str -t $clip_duration -c copy $output_file
    Write-Output "Completed clip ${i + 1} of ${num_clips}: ${output_file}"
}

$output_files -join " "
