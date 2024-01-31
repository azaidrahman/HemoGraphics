from aiogram import types
from aiogram.filters import Command
from io import BytesIO
from plot_trends import plot_retention, plot_trends
from aiogram.types import  BufferedInputFile

def register_handlers(dp,bot):

    
    @dp.message(Command('monthly_donation'))
    async def monthly_donations(message: types.Message):
        await message.answer("Request received! Hold on one moment while I load it up")
        
        buf = plot_trends("donations_state","monthly_donations")
        if buf and isinstance(buf, BytesIO):
            print('Buffer is loaded')
            buf.seek(0)
            photo = BufferedInputFile(buf.getvalue(), filename="chart.png")  # Convert buffer to InputFile
            await bot.send_photo(message.chat.id, photo=photo, caption="Latest Blood Donation Trends among states")
            buf.close()  # Close the buffer after sending the photo
        else:
            print("Buffer is empty or not a BytesIO instance")

            
    @dp.message(Command('seasonal'))
    async def seasonal_chart(message: types.Message):
        await message.answer("Request received! Hold on one moment while I load it up")
        buffers = plot_trends("donations_state","seasonal")
        for state, buf in buffers.items():
            if buf and isinstance(buf, BytesIO):
                buf.seek(0)
                photo = BufferedInputFile(buf.getvalue(), filename="chart.png")  # Convert buffer to InputFile
                await bot.send_photo(message.chat.id, photo=photo)
                buf.close()  # Close the buffer after sending the photo
            else:
                print("Buffer is empty or not a BytesIO instance")

    @dp.message(Command('retention'))
    async def retention_chart(message: types.Message):
        await message.answer("Request received for retention! Hold on one moment while I load it up\n\n This one will take awhile! (Roughly 45 seconds)")
        buf = plot_retention() 
        if buf and isinstance(buf, BytesIO):
            print('Buffer is loaded')
            buf.seek(0)
            photo = BufferedInputFile(buf.getvalue(), filename="chart.png")  # Convert buffer to InputFile
            await bot.send_photo(message.chat.id, photo=photo, caption="Latest Blood Donation Trends among states")
            buf.close()  # Close the buffer after sending the photo
        else:
            print("Buffer is empty or not a BytesIO instance")
    
    @dp.message(Command('chart'))
    async def chart_command(message: types.Message):
        await message.answer("Generating charts... Please wait")
        
        await monthly_donations(message)
        await seasonal_chart(message)
        await retention_chart(message)
        
        await message.answer("All charts have been sent!")

        outro_message = ("Thank you for engaging with the HemoGraphics blood donation data analysis. To delve deeper into the project or to explore more of our work, visit our GitHub repository:\n\n"
                         
                         "🌐 HemoGraphics on GitHub: https://github.com/azaidrahman/HemoGraphics\n"
                         
                         "📞 Contact: +60132352745"
                         
                         )
        await message.answer(outro_message)