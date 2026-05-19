vim.g.mapleader = " "
local keymap = vim.keymap

keymap.set("n", "<leader>nh", ":nohl<CR>", { desc = "Clear search highlights" })

-- delete single character without copying into register
-- keymap.set("n", "x", '"_x')

-- increment/decrement numbers
keymap.set("n", "<leader>+", "<C-a>", { desc = "Increment number" }) -- increment
keymap.set("n", "<leader>-", "<C-x>", { desc = "Decrement number" }) -- decrement

-- window management
keymap.set("n", "<leader>sv", "<C-w>v", { desc = "Split window vertically" }) -- split window vertically
keymap.set("n", "<leader>sh", "<C-w>s", { desc = "Split window horizontally" }) -- split window horizontally
keymap.set("n", "<leader>se", "<C-w>=", { desc = "Make splits equal size" }) -- make split windows equal width & height
keymap.set("n", "<leader>sx", "<cmd>close<CR>", { desc = "Close current split" }) -- close current split window

keymap.set("n", "<leader>to", "<cmd>tabnew<CR>", { desc = "Open new tab" }) -- open new tab
keymap.set("n", "<leader>tx", "<cmd>tabclose<CR>", { desc = "Close current tab" }) -- close current tab
keymap.set("n", "<leader>tn", "<cmd>tabn<CR>", { desc = "Go to next tab" }) --  go to next tab
keymap.set("n", "<leader>tp", "<cmd>tabp<CR>", { desc = "Go to previous tab" }) --  go to previous tab
keymap.set("n", "<leader>tf", "<cmd>tabnew %<CR>", { desc = "Open current buffer in new tab" }) --  move current buffer to new tab

-- buffer shortcuts
keymap.set("n", "<leader>b1", "<cmd>BufferLineGoToBuffer 1<CR>", { desc = "Open first visible tab on buffer line" })
keymap.set("n", "<leader>b2", "<cmd>BufferLineGoToBuffer 2<CR>", { desc = "Open second visible tab on buffer line" })
keymap.set("n", "<leader>b3", "<cmd>BufferLineGoToBuffer 3<CR>", { desc = "Open third visible tab on buffer line" })
keymap.set("n", "<leader>b4", "<cmd>BufferLineGoToBuffer 4<CR>", { desc = "Open fourth visible tab on buffer line" })
keymap.set("n", "<leader>b5", "<cmd>BufferLineGoToBuffer 5<CR>", { desc = "Open fifth visible tab on buffer line" })
keymap.set("n", "<leader>b6", "<cmd>BufferLineGoToBuffer 6<CR>", { desc = "Open sixth visible tab on buffer line" })
keymap.set("n", "<leader>b7", "<cmd>BufferLineGoToBuffer 7<CR>", { desc = "Open seventh visible tab on buffer line" })
keymap.set("n", "<leader>b8", "<cmd>BufferLineGoToBuffer 8<CR>", { desc = "Open eighth visible tab on buffer line" })
keymap.set("n", "<leader>b9", "<cmd>BufferLineGoToBuffer 9<CR>", { desc = "Open ninth visible tab on buffer line" })
keymap.set("n", "<leader>bl", "<cmd>BufferLineGoToBuffer -1<CR>", { desc = "Open last visible tab on buffer line" })
keymap.set("n", "<leader>bn", "<cmd>BufferLineCycleNext<CR>", { desc = "Cycle next buffer" })
keymap.set("n", "<leader>bp", "<cmd>BufferLineCyclePrev<CR>", { desc = "Cycle previous buffer" })

keymap.set("n", "<leader>bcl", "<cmd>BufferLineCloseLeft<CR>", { desc = "Close all buffers left of current" })
keymap.set("n", "<leader>bco", "<cmd>BufferLineCloseOthers<CR>", { desc = "Close all other buffers" })
keymap.set("n", "<leader>bcr", "<cmd>BufferLineCloseRight<CR>", { desc = "Close all buffers right of current" })
