# aspire-cosmos-python-web

Demo .NET Aspire project with Cosmos DB, Python backend and static web front end

## How it was created

```pwsh
dotnet new install Aspire.ProjectTemplates

dotnet add package Aspire.Hosting.Azure.CosmosDB
```

[Add Cosmos Db emulator](https://learn.microsoft.com/en-us/dotnet/aspire/database/azure-cosmos-db-integration?tabs=dotnet-cli&WT.mc_id=DOP-MVP-5001655#add-azure-cosmos-db-emulator-resource)

```csharp
var cosmos = builder.AddAzureCosmosDB("cosmos-db")
                    .RunAsEmulator();
```
