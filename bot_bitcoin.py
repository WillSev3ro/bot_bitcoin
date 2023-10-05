import websocket
import ssl
import json
import bitstamp.client
import credenciais

def cliente():
    return bitstamp.client.Trading(username = credenciais.USERNAME,
                                   key = credenciais.KEY, 
                                   secret = credenciais.SECRET)


def comprar(quantidade):
    trading_client = cliente()
    trading_client.buy_market_order(quantidade)

def vender(quantidade):
    trading_client = cliente()
    trading_client.sell_market_order(quantidade)


def ao_abir(ws):
    
    print('Conexão iniciada.')

    json_subscribe = """
    {
        "event": "bts:subscribe",
        "data": {
            "channel": "live_trades_btcusd"
        }
    }
"""
    ws.send(json_subscribe)

def ao_fechar(ws, close_status_code, close_msg):
    print('### Conexão encerrada. ###')




def ao_receber_mensagem(ws, mensagem):
    mensagem = json.loads(mensagem)
    price = mensagem['data']['price']
    print(price)

    if price > 28000:
        vender()
    
    elif price < 27400:
        comprar()
    
    else:
        print("Aguardar!")


def erro(ws, erro):
    print('Deu ruim!!')
    print(erro)

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws.bitstamp.net.", on_open=ao_abir, on_close=ao_fechar, on_message=ao_receber_mensagem, on_error=erro)
    
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
