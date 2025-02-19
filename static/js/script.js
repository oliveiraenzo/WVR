$(document).ready(function() {
    $('#scanForm').on('submit', function(event) {
        event.preventDefault();  // Impede o envio do formulário tradicional

        var searchQuery = $('#search_query').val();

        // Enviar a requisição AJAX para o back-end Flask
        $.ajax({
            url: '/scan',
            method: 'POST',
            data: { search_query: searchQuery },
            success: function(response) {
                // Limpar resultados antigos
                $('#results').empty();

                // Mostrar os novos resultados
                if (response.length > 0) {
                    var resultsHtml = '<ul>';
                    response.forEach(function(item) {
                        resultsHtml += '<li>';
                        resultsHtml += '<strong>IP:</strong> ' + item.IP + '<br>';
                        resultsHtml += '<strong>Provider:</strong> ' + item.Provider + '<br>';
                        resultsHtml += '<strong>ASN:</strong> ' + item.ASN + '<br>';
                        resultsHtml += '<strong>Location:</strong> ' + item.Location + '<br>';
                        resultsHtml += '<strong>Last Updated:</strong> ' + item['Last Updated'] + '<br>';
                        resultsHtml += '<strong>Services:</strong> ' + item.Services.join(', ') + '<br>';
                        resultsHtml += '</li>';
                    });
                    resultsHtml += '</ul>';
                    $('#results').html(resultsHtml);
                } else {
                    $('#results').html('<p>Nenhum resultado encontrado.</p>');
                }
            },
            error: function() {
                alert('Erro ao processar a requisição.');
            }
        });
    });
});
