Set-Location -Path "$PSScriptRoot"
for ($i = 1; $i -le 40; $i++) {
    $txtFile = "feature_$i.txt"
    $pptFile = "feature_$i.pptx"
    $docFile = "feature_$i.docx"
    $content = "Feature $i implementation details:\n\nThis feature adds XYZ functionality to the project. It includes the necessary code, documentation, and presentation slides.\n\n* Detailed description of the algorithm or UI changes.\n* Expected impact and usage examples.\n"
    # Overwrite the files with the detailed content
    Set-Content -Path $txtFile -Value $content -Encoding UTF8
    Set-Content -Path $pptFile -Value $content -Encoding UTF8
    Set-Content -Path $docFile -Value $content -Encoding UTF8
}
