validate mcp server is installed and running
validate api server is installed and running
validate end-to-end use case with following script:
{
    $body = @{
    architecture_description = "A simple web application with a load balancer, two web servers, and a database"
    output_format = "png"
    layout_direction = "TB"
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "http://localhost:8000/generate-diagram" -Method Post -Body $body -ContentType "application/json"

    Write-Host "Response received successfully!"
    Write-Host "Image format: $($response.image_format)"
    Write-Host "Image data length: $($response.image_data.Length) characters"
}