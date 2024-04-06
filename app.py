from flask import Flask, jsonify, request


app = Flask(__name__)


# Lista de objetos usuario
usuarios = []


class Usuario:
    def __init__(self, id, username, email, age, country):
        self.id = id
        self.username = username
        self.email = email
        self.age = age
        self.country = country

    def retorna_usuario(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'age': self.age,
            'country': self.country
        }


    @staticmethod
    def recebe_usuario(data):
        return Usuario(
            id=data.get('id'),
            username=data.get('username'),
            email=data.get('email'),
            age=data.get('age'),
            country=data.get('country')
        )


@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    # Retorna todos os usuários
    return jsonify([usuario.retorna_usuario() for usuario in usuarios])


@app.route('/usuarios/<int:id>', methods=['GET'])
def get_usuario_id(id):
    # Procura um usuário com o id informado
    for usuario in usuarios:
        if usuario.id == id:
            return jsonify(usuario.retorna_usuario())

    # Se o usuário não for encontrado retorna erro
    return jsonify({'error': 'Usuário não encontrado'}), 404


@app.route('/usuarios', methods=['POST'])
def post_usuario():
    # Recebe os dados do novo usiario
    novo_usuario_data = request.json

    # Cria um novo objeto usuario com os dados fornecidos
    novo_usuario = Usuario(
        id=novo_usuario_data['id'],
        username=novo_usuario_data['username'],
        email=novo_usuario_data['email'],
        age=novo_usuario_data['age'],
        country=novo_usuario_data['country']
    )

    # Adiciona o novo usuário à lista de usuários
    usuarios.append(novo_usuario)

    # Retorna o novo usuário e o status 201
    return jsonify(novo_usuario.retorna_usuario()), 201


@app.route('/usuarios/<int:id>', methods=['PUT'])
def put_ususario(id):
    usuario_alterado_data = request.get_json()
    for indice, usuario in enumerate(usuarios):
        if usuario.id == id:
            # Convertendo os dados JSON em um objeto Usuario
            usuario_alterado = Usuario.recebe_usuario(usuario_alterado_data)
            # Atualizando o usuário na lista de usuários
            usuarios[indice] = usuario_alterado
            return jsonify(usuario_alterado.retorna_usuario()), 200
    # Se o usuário não for encontrado retorna erro
    return jsonify({'message': 'Usuário não encontrado'}), 404


@app.route('/usuarios/<int:id>', methods=['DELETE'])
def delete_usuario(id):
    # Preciso acessar a variável global usuarios
    global usuarios

    # Procura um usuário com o id informado
    for indice, usuario in enumerate(usuarios):
        if usuario.id == id:
            # Remove o usuário da lista
            del usuarios[indice]
            # Retorna uma mensagem indicando o sucesso dessa operção
            return jsonify({'message': 'Usuário removido com sucesso'}), 200

    # Se o usuário não for encontrado retorna erro
    return jsonify({'error': 'Usuário não encontrado'}), 404


if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=True)