using System;
using NJsonSchema.CodeGeneration.Models;
using NJsonSchema.CodeGeneration.CSharp;
using NJsonSchema;
using System.Threading.Tasks;
using System.Linq;


namespace CSharpModelGenerator
{
    class Program
    {
        static async Task Main(string[] args)
        {
            var inputSchema = args[0];
            var outputFile = args[1];

            var schemaContents = System.IO.File.ReadAllText(inputSchema);
            var schema = await JsonSchema.FromJsonAsync(schemaContents);
            var generatorSettings = new CSharpGeneratorSettings() { Namespace = "com.silabs.utf.models" };
            

            System.IO.File.WriteAllText(outputFile, "");
            
            foreach(var typeName in schema.Definitions.Keys)
            {
                var type = schema.Definitions[typeName];
                type.Title = typeName;
                var generator = new CSharpGenerator(type, generatorSettings);
                var fileContents = generator.GenerateFile();
                
                var currentContents = System.IO.File.ReadAllText(outputFile);
                currentContents += "\n" + fileContents;
                System.IO.File.WriteAllText(outputFile, currentContents);
            }
        }
    }
}
