// /routes/itemRoutes.js
const express = require('express');
const router = express.Router();
const itemController = require('../controllers/itemController');

// POST /items - Create a new item
router.post('/items', itemController.createItem);

// GET /items - Get all items
router.get('/items', itemController.getAllItems);

// GET /items/:id - Get item by ID
router.get('/items/:id', itemController.getItemById);

// PUT /items/:id - Update item by ID
router.put('/items/:id', itemController.updateItem);

// DELETE /items/:id - Delete item by ID
router.delete('/items/:id', itemController.deleteItem);

module.exports = router;
