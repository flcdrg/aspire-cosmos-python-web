var builder = DistributedApplication.CreateBuilder(args);

var cosmos = builder.AddAzureCosmosDB("cosmos-db")
    .RunAsEmulator(emulator =>
    {
        emulator.WithDataVolume();
    });

#pragma warning disable ASPIREHOSTINGPYTHON001 // Type is for evaluation purposes only and is subject to change or removal in future updates. Suppress this diagnostic to proceed.
var pythonApp = builder.AddPythonApp("python-app", "../PythonApp", "main.py")
    .WithReference(cosmos)
    .WithEndpoint(env: "PORT", port: 8000);
#pragma warning restore ASPIREHOSTINGPYTHON001

builder.Build().Run();
