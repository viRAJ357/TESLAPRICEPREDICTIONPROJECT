Set-Location -Path "$PSScriptRoot"
for ($i=1; $i -le 40; $i++) {
    $featureFile = "feature_$i.txt"
    $pptFile = "feature_$i.pptx"
    $docFile = "feature_$i.docx"
    "Feature $i implementation details." | Out-File -Encoding utf8 $featureFile
    "Placeholder PPT content for feature $i." | Out-File -Encoding utf8 $pptFile
    "Placeholder DOC content for feature $i." | Out-File -Encoding utf8 $docFile
    git add $featureFile $pptFile $docFile
    git commit -m "feat: add feature $i with PPT and DOC"
}
