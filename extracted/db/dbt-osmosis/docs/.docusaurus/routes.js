import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/dbt-osmosis/markdown-page',
    component: ComponentCreator('/dbt-osmosis/markdown-page', 'a0f'),
    exact: true
  },
  {
    path: '/dbt-osmosis/docs',
    component: ComponentCreator('/dbt-osmosis/docs', '5e2'),
    routes: [
      {
        path: '/dbt-osmosis/docs',
        component: ComponentCreator('/dbt-osmosis/docs', '7ff'),
        routes: [
          {
            path: '/dbt-osmosis/docs',
            component: ComponentCreator('/dbt-osmosis/docs', 'acc'),
            routes: [
              {
                path: '/dbt-osmosis/docs/explanation/',
                component: ComponentCreator('/dbt-osmosis/docs/explanation/', '189'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/dbt-osmosis/docs/explanation/settings-resolution',
                component: ComponentCreator('/dbt-osmosis/docs/explanation/settings-resolution', '8b2'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/dbt-osmosis/docs/explanation/yaml-routing',
                component: ComponentCreator('/dbt-osmosis/docs/explanation/yaml-routing', 'e68'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/dbt-osmosis/docs/how-to/',
                component: ComponentCreator('/dbt-osmosis/docs/how-to/', 'b43'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/dbt-osmosis/docs/how-to/manage-sources',
                component: ComponentCreator('/dbt-osmosis/docs/how-to/manage-sources', '15a'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/dbt-osmosis/docs/how-to/review-changes',
                component: ComponentCreator('/dbt-osmosis/docs/how-to/review-changes', '4a7'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/dbt-osmosis/docs/intro',
                component: ComponentCreator('/dbt-osmosis/docs/intro', '3df'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/dbt-osmosis/docs/migrating',
                component: ComponentCreator('/dbt-osmosis/docs/migrating', 'd19'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/dbt-osmosis/docs/reference/',
                component: ComponentCreator('/dbt-osmosis/docs/reference/', 'f8e'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/dbt-osmosis/docs/reference/cli',
                component: ComponentCreator('/dbt-osmosis/docs/reference/cli', '6d9'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/dbt-osmosis/docs/reference/settings',
                component: ComponentCreator('/dbt-osmosis/docs/reference/settings', 'cd3'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/dbt-osmosis/docs/tutorial-basics/commands',
                component: ComponentCreator('/dbt-osmosis/docs/tutorial-basics/commands', 'a2f'),
                exact: true
              },
              {
                path: '/dbt-osmosis/docs/tutorial-basics/installation',
                component: ComponentCreator('/dbt-osmosis/docs/tutorial-basics/installation', '1cd'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/dbt-osmosis/docs/tutorial-yaml/configuration',
                component: ComponentCreator('/dbt-osmosis/docs/tutorial-yaml/configuration', 'ee1'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/dbt-osmosis/docs/tutorial-yaml/context',
                component: ComponentCreator('/dbt-osmosis/docs/tutorial-yaml/context', '812'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/dbt-osmosis/docs/tutorial-yaml/inheritance',
                component: ComponentCreator('/dbt-osmosis/docs/tutorial-yaml/inheritance', 'cf5'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/dbt-osmosis/docs/tutorial-yaml/selection',
                component: ComponentCreator('/dbt-osmosis/docs/tutorial-yaml/selection', '235'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/dbt-osmosis/docs/tutorial-yaml/synthesize',
                component: ComponentCreator('/dbt-osmosis/docs/tutorial-yaml/synthesize', '4cc'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/dbt-osmosis/docs/tutorial-yaml/workflow',
                component: ComponentCreator('/dbt-osmosis/docs/tutorial-yaml/workflow', 'e16'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/dbt-osmosis/docs/tutorials/',
                component: ComponentCreator('/dbt-osmosis/docs/tutorials/', 'e8f'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/dbt-osmosis/docs/tutorials/first-refactor',
                component: ComponentCreator('/dbt-osmosis/docs/tutorials/first-refactor', '229'),
                exact: true,
                sidebar: "docs"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/dbt-osmosis/',
    component: ComponentCreator('/dbt-osmosis/', '456'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
