-- .nvim.lua
vim.g.rustaceanvim = {
  server = {
    default_settings = {
      ["rust-analyzer"] = {
        cargo = {
          allFeatures = false,
          features = {  "all" },
        },
      },
    },
  },
}
