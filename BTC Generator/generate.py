from bip_utils import Bip39MnemonicGenerator, Bip39SeedGenerator, Bip86, Bip86Coins, Bip32Slip10Secp256k1
from openpyxl import Workbook

def generate_wallets(num_wallets):
    # Создание таблицы Excel
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Wallets"
    sheet['A1'] = "Address"
    sheet['B1'] = "Private Key"

    # Генерация кошельков
    for i in range(num_wallets):
        # Генерация мнемонической фразы (12 слов)
        mnemonic = Bip39MnemonicGenerator().FromWordsNumber(12)
        seed = Bip39SeedGenerator(mnemonic).Generate()
        
        # Генерация Taproot-адреса (P2TR) с использованием BIP-86
        bip86_ctx = Bip86.FromSeed(seed, Bip86Coins.BITCOIN)
        taproot_addr = bip86_ctx.PublicKey().ToAddress()
        
        # Получение закрытого ключа
        private_key = bip86_ctx.PrivateKey().Raw().ToHex()

        # Запись адреса и закрытого ключа в таблицу
        sheet[f'A{i + 2}'] = taproot_addr
        sheet[f'B{i + 2}'] = private_key  # Записываем закрытый ключ в таблицу
    
    # Сохранение таблицы в файл
    workbook.save("Wallet.xlsx")
    print(f"{num_wallets} кошельков успешно сгенерировано и сохранено в Wallet.xlsx")

if __name__ == "__main__":
    # Запрос количества кошельков для генерации
    num_wallets = int(input("Введите количество кошельков, которые нужно сгенерировать: "))
    generate_wallets(num_wallets)
