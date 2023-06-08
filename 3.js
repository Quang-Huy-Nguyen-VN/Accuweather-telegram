const TelegramBot = require("node-telegram-bot-api");
const axios = require("axios");
// const express = require('express');
// const app = express();
const token = "5767090979:AAFyHPOf7AA4YZTH8hcerFyRz6A9hihoS1M";
const bot = new TelegramBot(token, { polling: true });

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//FUNCTION SEARCHING//
const GOOGLE_API_KEY = 'AIzaSyDWfmdHdFTwsVOlSJdIkmf0q-gIR7mvqCQ'; //API KEY GOOGLE
const SEARCH_ENGINE_ID = 'a0390e5337ea64b5e'; //API KEY GOOGLE SEARCHING ENGINE

bot.onText(/\/timkiem (.+)/, async (message, match) => {
  const chatId = message.chat.id;
  const searchQuery = match[1];

  axios.get('https://www.googleapis.com/customsearch/v1', {
      params: {
        key: GOOGLE_API_KEY,
        cx: SEARCH_ENGINE_ID,
        q: searchQuery,
      },
    })
    .then((response) => {
      const searchResults = response.data.items;

      if (searchResults && searchResults.length > 0) {
        let message = '';

        for (const result of searchResults) {
          message += `${result.title}\n${result.link}\n\n`;
        }

        bot.sendMessage(chatId, message);
      } else {
        bot.sendMessage(chatId, 'Không tìm thấy kết quả.');
      }
    })
    .catch((error) => {
      console.error('Lỗi tìm kiếm:', error);
      bot.sendMessage(chatId, 'Đã xảy ra lỗi khi tìm kiếm dữ liệu.');
    });
});
