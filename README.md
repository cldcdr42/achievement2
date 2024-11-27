# achievement2

hse_buildingDistributedSystems_fall_2024

Component and Sequence diagram for easy and medium difficulty task for achievement 2

Some code for hard difficulty task

# To run app

python app.py

# To send request (using windows powershell)

Invoke-WebRequest -Uri "http://127.0.0.1:5000/process" `
>>                   -Method POST `
>>                   -Headers @{"Content-Type" = "application/json"} `
>>                   -Body '{"number": 1}'

Replace 1 with any other natural number
