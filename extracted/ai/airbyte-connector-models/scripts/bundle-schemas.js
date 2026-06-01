#!/usr/bin/env node

/**
 * Bundle JSON schemas using @apidevtools/json-schema-ref-parser
 * This script resolves all $ref references in the schema files and creates bundled schemas.
 *
 * Supports two entry points:
 * 1. ConnectorMetadataDefinitionV0 - for individual connector metadata.yaml validation
 * 2. ConnectorRegistryV0 - for full registry JSON validation
 */

const $RefParser = require('@apidevtools/json-schema-ref-parser');
const fs = require('fs');
const path = require('path');

const YAML_DIR = 'src/metadata/v0';
const OUTPUT_DIRS = [
  'models/metadata/v0',
  'airbyte_connector_models/metadata/v0',
];

const SCHEMAS = [
  {
    name: 'ConnectorMetadataDefinitionV0',
    entryFile: 'ConnectorMetadataDefinitionV0.yaml',
    outputJson: 'ConnectorMetadataDefinitionV0.json',
    newId: 'https://raw.githubusercontent.com/airbytehq/airbyte-connector-models/main/models/metadata/v0/ConnectorMetadataDefinitionV0.json'
  },
  {
    name: 'ConnectorRegistryV0',
    entryFile: 'ConnectorRegistryV0.yaml',
    outputJson: 'ConnectorRegistryV0.json',
    newId: 'https://raw.githubusercontent.com/airbytehq/airbyte-connector-models/main/models/metadata/v0/ConnectorRegistryV0.json'
  }
];

async function bundleSchema(schemaConfig) {
  const entrySchema = path.join(YAML_DIR, schemaConfig.entryFile);

  console.log(`\n📦 Bundling ${schemaConfig.name}...`);
  console.log(`   Entry schema: ${entrySchema}`);

  if (!fs.existsSync(entrySchema)) {
    console.error(`❌ Error: Entry schema does not exist: ${entrySchema}`);
    return false;
  }

  for (const outputDir of OUTPUT_DIRS) {
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }
  }

  try {
    const schema = await $RefParser.bundle(entrySchema, {
      dereference: {
        circular: 'ignore'
      }
    });

    schema.$id = schemaConfig.newId;
    const serialized = JSON.stringify(schema, null, 2) + '\n';

    for (const outputDir of OUTPUT_DIRS) {
      const bundleOutput = path.join(outputDir, schemaConfig.outputJson);
      fs.writeFileSync(bundleOutput, serialized);
      console.log(`✅ Wrote bundled schema to ${bundleOutput}`);
    }
    console.log(`   Updated $id to: ${schemaConfig.newId}`);

    return true;
  } catch (error) {
    console.error(`❌ Error bundling ${schemaConfig.name}:`, error.message);
    return false;
  }
}

async function bundleAllSchemas() {
  console.log('📦 Bundling all JSON schemas...');

  let successCount = 0;
  let failCount = 0;

  for (const schemaConfig of SCHEMAS) {
    const success = await bundleSchema(schemaConfig);
    if (success) {
      successCount++;
    } else {
      failCount++;
    }
  }

  console.log(`\n✅ Bundling complete: ${successCount} succeeded, ${failCount} failed`);

  if (failCount > 0) {
    process.exit(1);
  }
}

bundleAllSchemas();
