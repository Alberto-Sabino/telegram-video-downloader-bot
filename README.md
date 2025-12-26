# Desenvolvimento com Docker (container temporário)

Este projeto inclui um `Dockerfile` mínimo que instala o runtime Python e os pacotes listados em `requirements.txt`.

Use o helper `dev.sh` fornecido para construir a imagem e executar um container temporário para desenvolvimento.

Comandos rápidos

- Build da imagem e abrir um shell dentro de um container temporário:

```bash
./dev.sh
```

- Executar os testes dentro de um container temporário (não interativo):

```bash
./dev.sh pytest -q
```

- Executar um comando Python pontual dentro do container:

```bash
./dev.sh python -m pip list
```

Notas e dicas

- O helper monta seu diretório de projeto em `/app` dentro do container. Quaisquer alterações de arquivo que você fizer no host ficam imediatamente visíveis dentro do container.
- O `Dockerfile` já executa `pip install -r requirements.txt` durante a construção da imagem. Se você adicionar novas dependências, reexecute `./dev.sh` para reconstruir.
- A porta `8000` está exposta (o `docker run` a publica para o host) — ajuste ou adicione portas se a sua app precisar de outras.
- A imagem do container é efêmera: `--rm` remove o container após a saída. Use `docker run` sem `--rm` se quiser manter containers.

Solução de problemas

- Se o Docker Desktop/Engine não estiver rodando na sua máquina, inicie-o primeiro.
- No Windows com WSL, certifique-se de que a integração do Docker com o WSL está habilitada ou use o engine do Docker disponível ao WSL.

Se quiser, eu também posso:

- Adicionar um `docker-compose.dev.yml` com um serviço bind-mounted e um `Makefile` com comandos curtos.
- Modificar o `Dockerfile` para incluir ferramentas de desenvolvimento (git, build-essential) ou um usuário não-root.
- Adicionar um workflow do GitHub Actions que execute os testes automaticamente dentro desta imagem.
