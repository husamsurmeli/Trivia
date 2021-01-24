import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import '../stylesheets/App.css';

class Documentation extends Component {
    render(){
        return (
            <table>
            <tr>
              <th>Endpoints</th>
              <th>.</th>
              <th>.</th>
              <th>Description</th>
              <th>.</th>
              <th>.</th>
              <th>Requests</th>
              <th>.</th>
              <th>.</th>
              <th>Returns</th>
            </tr>
            <tr>
              <td><code>GET '/categories'</code></td>
              <td>.</td>
              <td>.</td>
              <td>queries all categories</td>
              <td>.</td>
              <td>.</td>
              <td>None on the user end</td>
              <td>.</td>
              <td>.</td>
              <td>json data of <code>'success': ,'categories':</code></td>
            </tr>
            <tr>
              <td><code>GET '/questions'</code></td>
              <td>.</td>
              <td>.</td>
              <td>queries all categories</td>
              <td>.</td>
              <td>.</td>
              <td>None on the user end</td>
              <td>.</td>
              <td>.</td>
              <td>json data of <code>'success': ,'questions':, 'total_questions':, 'categories':, 'current_category':</code></td>
            </tr>
            <tr>
              <td><code>DELETE '/questions/{'<'}int:question_id{'>'}'</code></td>
              <td>.</td>
              <td>.</td>
              <td>deletes a single question</td>
              <td>.</td>
              <td>.</td>
              <td>question_id as an integer</td>
              <td>.</td>
              <td>.</td>
              <td>json data of <code>'success': ,'questions':, 'total_questions':</code></td>
            </tr>
            <tr>
              <td><code>POST '/questions'</code></td>
              <td>.</td>
              <td>.</td>
              <td>creates new question</td>
              <td>.</td>
              <td>.</td>
              <td>json data of <code>'question':, answer', 'difficulty', 'category',</code></td>
              <td>.</td>
              <td>.</td>
              <td>json data of <code>'success': ,'questions':, 'total_questions':</code></td>
            </tr>
            <tr>
              <td><code>POST '/questions/search'</code></td>
              <td>.</td>
              <td>.</td>
              <td>question search</td>
              <td>.</td>
              <td>.</td>
              <td>json data of <code>'searchTerm':</code></td>
              <td>.</td>
              <td>.</td>
              <td>json data of <code>'success': ,'questions':, 'total_questions':</code></td>
            </tr>
            <tr>
              <td><code>GET '/categories/{'<'}int:category_id{'>'}/questions'</code></td>
              <td>.</td>
              <td>.</td>
              <td>gets questions on the spesific category</td>
              <td>.</td>
              <td>.</td>
              <td>category_id as an integer</td>
              <td>.</td>
              <td>.</td>
              <td>json data of <code>'success': ,'questions':, 'total_questions':, 'current_category':</code></td>
            </tr>
            <tr>
              <td><code>POST '/quiz'</code></td>
              <td>.</td>
              <td>.</td>
              <td>gets questions random sequentially (max 5 of them in a game) based on all categories or just one</td>
              <td>.</td>
              <td>.</td>
              <td>json data of <code>'quiz_category': ,'previous_questions':</code></td>
              <td>.</td>
              <td>.</td>
              <td>json data of <code>'success': ,'questions':</code></td>
            </tr>
          </table>
          );

    }
}
export default Documentation;