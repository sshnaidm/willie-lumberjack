% least = 9
% pre_line = 3

      <p>
      <div class="jumbotron">
        <h1>{{project}}</h1>
        <p>A logging module for Willie IRC bot with real-time log viewer.</p>
          <a class="btn btn-lg btn-primary" href="#">Read more &raquo;</a>
        </p>
      </div>
      <div class="row">
        % i = 0
        % if status:
          % for s in status:
        <a href="/channel/{{s['name']}}/">
        <div class="col-md-4">
          <div class="panel panel-default">
            <div class="panel-heading">
              <h3 class="panel-title">#{{s['name']}}</h3>
            </div>
            <div class="panel-body">
              <p>{{s['length']}} messages.</p>
            </div>
          </div>
        </div>
        </a>
            % i += 1
            % if i >= pre_line:
              % i = 0
      </div>
      <div class="row">
            % end
            
          % end
        % end

        % if len(channels) < least:
            % for x in xrange(least - len(channels)):
        <div class="col-md-4">
          <div class="panel panel-default">
            <div class="panel-heading">
              <h3 class="panel-title">None</h3>
            </div>
            <div class="panel-body">
              <p>...</p>
            </div>
          </div>
        </div>
            % i += 1
            % if i >= pre_line:
              % i = 0
      </div>
      <div class="row">
            % end
        % end
      </div>

% rebase layout title='channels', project=project, channel=None, channels=channels
