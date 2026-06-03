executar = True
while executar :
    anoNasc = int(input ('em que ano você nasceu?\nR: '))
    anoAtual = int(input ('em que ano estamos?\nR:'))
    idade = anoAtual - anoNasc
    print('Você tem: ' + str(idade) + ' anos')
    opcao =input('\nDeseja testar novamente? \n[1]Sim \n[2]Não\nR: ')
    if opcao == "2" or opcao == "Não":
        executar = False
    