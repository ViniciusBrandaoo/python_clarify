from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1> Olá mundo! </h1> <br> <h2>sou um subtitulo Desenvolvido pelo Vinicius</h2> </h3>caso encontre um bug me avise!!</h3>"

@app.route('/sobre')
def sobre ():
    return '''
    <!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Sobre</title><style>*{margin:0;padding:0;box-sizing:border-box}body{display:flex;justify-content:center;align-items:center;min-height:100vh;background:linear-gradient(135deg,#0f172a,#1e293b,#334155);font-family:Arial,sans-serif;overflow:hidden}.card{background:rgba(255,255,255,0.08);backdrop-filter:blur(10px);padding:40px;border-radius:20px;text-align:center;color:#fff;max-width:600px;box-shadow:0 10px 30px rgba(0,0,0,0.3);animation:fadeUp 1s ease}.card h1{font-size:2.5rem;margin-bottom:15px;background:linear-gradient(90deg,#38bdf8,#818cf8);-webkit-background-clip:text;-webkit-text-fill-color:transparent}.card p{font-size:1.1rem;line-height:1.7;color:#e2e8f0}.glow{position:absolute;width:300px;height:300px;background:radial-gradient(circle,rgba(56,189,248,0.3),transparent 70%);border-radius:50%;animation:float 6s ease-in-out infinite}.glow:nth-child(1){top:-100px;left:-100px}.glow:nth-child(2){bottom:-100px;right:-100px;animation-delay:3s}@keyframes fadeUp{from{opacity:0;transform:translateY(30px)}to{opacity:1;transform:translateY(0)}}@keyframes float{0%,100%{transform:translateY(0) translateX(0)}50%{transform:translateY(20px) translateX(20px)}}</style></head><body><div class="glow"></div><div class="glow"></div><div class="card"><h1>Sobre o Desenvolvedor</h1><p>Olá! Meu nome é Vinicius Brandão e sou desenvolvedor apaixonado por tecnologia, criação de interfaces modernas e desenvolvimento de soluções eficientes. Estou sempre buscando aprender novas ferramentas, aprimorar minhas habilidades e transformar ideias em projetos funcionais e elegantes.</p></div></body></html>
'''

@app.route('/ola/<nome>')
def ola(nome):
    return f"<h1>Olá {nome}</h1>"

if __name__ == '__main__':
    app.run(debug=True)