
        vapour.directive('dropList', function () {
            var htmlTemplate = '<div ng-class="className" > ' +
                    '<button class="btn btn-default" type="button" data-toggle="dropdown"  ng-click="changeState()">  ' +
                    '{{text}} <span class="caret"></span>' +
                    '</button> ' +
                    '<ul class="dropdown-menu" role="menu" ng-style="stateStyle"> ' +
                    '<li ng-repeat="item in data track by $index" ><a href="javascript:;" ng-click="listClick(item)">{{item.values}}</a></li> ' +
                    '</ul>' +
                    '</div>';
            return {
                template: htmlTemplate,
                replace: true,
                scope: {
                    data: '=',
                    active: '=',
                    className: '@'
                },
                link: function($scope) {
                    if (!$scope.data || !$scope.data.length) {
                        return false;
                    }
                    $scope.className = $scope.className || 'btn-group';
                    $scope.state = false;
                    $scope.stateStyle = {
                        display: 'none'
                    };
                    $scope.data.forEach(function (v) {
                        if (v.key === $scope.active) {
                            $scope.text = v.values;
                        }
                    });
                    $scope.listClick = function (item) {
                        $scope.active = item.key;
                        $scope.text = item.values;
                        $scope.state = false;
                        changeStyle();
                    };
                    $scope.changeState = function () {
                        $scope.state = !$scope.state;
                        changeStyle();
                    };
                    function changeStyle () {
                        if ($scope.state) {
                            $scope.stateStyle = {
                                display: 'inline-block'
                            };
                        } else {
                            $scope.stateStyle = {
                                display: 'none'
                            };
                        }
                    }
                }
            }
        });
        vapour.directive('dropListGroup', function () {
            var htmlTemplate = '<div><div class="input-group" ng-repeat="item in data track by $index">' +
                    '<div drop-list class-name="input-group-btn" data="setData" active="item.type"></div>' +
                    '<input type="text" style="width: 300px; margin-right: 20px;" ng-model="item.values" class="form-control">' +
                    '<button type="button" class="btn btn-danger" ng-click="deleteItem($index)">' +
                    '<span class="glyphicon glyphicon-remove"></span> 删除' +
                    '</button>' +
                    '</div></div>';
            return {
                template: htmlTemplate,
                replace: true,
                scope: {
                    data: '=',
                    active: '='
                },
                link: function($scope) {
                    if (!$scope.data || !$scope.data.length) {
                        return false;
                    }
                    $scope.setData = [
                        {
                            key: 'String',
                            values: 'String'
                        },
                        {
                            key: 'Long',
                            values: 'Long'
                        },
                        {
                            key: 'Double',
                            values: 'Double'
                        },
                        {
                            key: 'Date',
                            values: 'Date'
                        },
                        {
                            key: 'Boolean',
                            values: 'Boolean'
                        },
                        {
                            key: 'Bytes',
                            values: 'Bytes'
                        },

                    ];
                    $scope.deleteItem = function (index) {
                        $scope.data.splice(index, 1);
                    }
                }
            }
        });
