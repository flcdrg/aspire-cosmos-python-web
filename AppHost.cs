var builder = DistributedApplication.CreateBuilder(args);

#pragma warning disable ASPIRECOSMOSDB001

var cosmos = builder.AddAzureCosmosDB("cosmos-db").RunAsPreviewEmulator(
                     emulator =>
                     {
                         emulator.WithDataExplorer();
                         emulator.WithDataVolume();
                     });

builder.Build().Run();
